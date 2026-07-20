import sys
from pathlib import Path

# --- Make sure the project root (parent of backend/) is importable,
#     regardless of the working directory uvicorn was started from. ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Database
from ai.interpreter import Interpreter, UnsupportedRequestError, InterpreterError
from ai.executor import Executor

from backend.models import ChatRequest, ChatResponse


app = FastAPI(
    title="AI Database Assistant API",
    description="Thin HTTP layer over the existing Interpreter/Executor/Database pipeline.",
    version="1.0.0",
)

# Dev-friendly CORS for the Vite frontend (default port 5173).
# Tighten allow_origins before deploying anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single shared instances -- created once at startup, reused across
# requests (mirrors how the CLI / Streamlit app use them).
db = Database(str(PROJECT_ROOT / "data" / "mydb.json"))
interpreter = Interpreter()
executor = Executor(db)


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """Simple liveness check -- not part of the required spec, but
    useful for confirming the server + imports loaded correctly."""
    return {"status": "ok", "tables": db.list_tables()}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Takes a natural language message, runs it through the existing
    Interpreter -> Executor pipeline, and returns the result.

    Never raises HTTP error codes for "expected" failure modes
    (unsupported request, bad command, validation error) -- those are
    returned as success=false with a message, so the frontend can
    render them as a red assistant bubble per spec, instead of having
    to handle both HTTP errors AND success=false separately.
    """

    message = request.message.strip()

    if not message:
        return ChatResponse(
            success=False,
            message="Please enter a message.",
            data=None,
        )

    try:
        command = interpreter.interpret(message)
        result = executor.execute(command)

        return ChatResponse(
            success=result.get("success", True),
            message=result.get("message", "Done."),
            data=result.get("data"),
        )

    except UnsupportedRequestError:
        return ChatResponse(
            success=False,
            message=(
                "I couldn't match that to a database action. Try "
                "rephrasing -- e.g. \"show all students\" or "
                "\"delete students with marks below 40\"."
            ),
            data=None,
        )

    except InterpreterError as e:
        return ChatResponse(
            success=False,
            message=f"I had trouble understanding that: {e}",
            data=None,
        )

    except ValueError as e:
        # Raised by Executor for missing/invalid required command fields
        return ChatResponse(
            success=False,
            message=str(e),
            data=None,
        )

    except Exception as e:
        # Last-resort catch so a bug never surfaces as a raw 500 with
        # no explanation on the frontend.
        return ChatResponse(
            success=False,
            message=f"Something went wrong: {e}",
            data=None,
        )
