from core.database import Database
from ai.interpreter import (
    Interpreter,
    UnsupportedRequestError,
    InterpreterError,
)
from ai.executor import Executor, UnsupportedActionError



def main():

    db = Database("data/mydb.json")

    interpreter = Interpreter()

    executor = Executor(db)

    print("=" * 60)
    print("      AI Database Assistant")
    print("=" * 60)
    print("Type your request in natural language.")
    print("Type EXIT to quit.\n")

    while True:

        user_input = input("AI-DB> ").strip()

        if not user_input:
            continue

        if user_input.upper() == "EXIT":
            print("Goodbye!")
            break

        try:

            command = interpreter.interpret(user_input)

            result = executor.execute(command)

            print("\nResult:")
            print(result)
            print()

        except UnsupportedRequestError as e:
            print(f"\nUnsupported Request: {e}\n")

        except InterpreterError as e:
            print(f"\nInterpreter Error: {e}\n")

        except Exception as e:
            print(f"\nExecution Error: {e}\n")

        except UnsupportedActionError as e:
            return ChatResponse(
                success=False,
                message=str(e),
                data=None
    )


if __name__ == "__main__":
    main()


