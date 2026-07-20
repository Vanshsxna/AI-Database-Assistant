"""
Pydantic models for the FastAPI backend.

These exist purely for request/response validation and API docs at
the HTTP boundary -- they do not replace or duplicate ai.schemas.Command,
which remains the single source of truth for the internal pipeline
(Interpreter -> Command -> Executor).
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Body of POST /chat."""

    message: str = Field(
        ...,
        min_length=1,
        description="Natural language instruction, e.g. 'show all students'.",
        examples=["add a student with id 1, name Vansh, marks 95"],
    )


class ChatResponse(BaseModel):
    """
    Response of POST /chat.

    Mirrors the {"success", "message", "data"} shape already returned
    by Database/Executor -- this model just gives it a typed, documented
    HTTP contract for the frontend to rely on.

    `data` is intentionally loose (Any) because it varies by action:
      - select        -> list[dict]  (rows)
      - insert        -> dict        (the inserted row)
      - update/count  -> dict/int
      - tables        -> list[str]
      - info          -> dict        (schema)
      - create/drop/truncate -> None
    """

    success: bool
    message: str
    data: Optional[Any] = None
