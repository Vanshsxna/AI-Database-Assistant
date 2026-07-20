from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import asdict
import json
import os
import re

from ai.prompts import SYSTEM_PROMPT
from ai.schemas import Command

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class UnsupportedRequestError(Exception):
    pass

class InterpreterError(Exception):
    pass


class Interpreter:

    MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    MAX_RETRIES = 2

    def interpret(self, user_input: str) -> Command:

        if not user_input or not user_input.strip():
            raise InterpreterError("Empty input provided.")

        last_error = None

        for attempt in range(self.MAX_RETRIES):

            try:
                raw_text = self._call_model(user_input)
                data = self._parse_json(raw_text)

                if "error" in data:
                    raise UnsupportedRequestError(
                        data.get("error", "Unsupported request.")
                    )

                data = self._apply_defaults(data)

                return Command(**data)

            except UnsupportedRequestError:
                raise

            except Exception as e:
                last_error = e

        raise InterpreterError(
            f"Failed to interpret command after "
            f"{self.MAX_RETRIES} attempts.\n"
            f"Last error: {last_error}"
        )

    def _call_model(self, user_input: str) -> str:
        response = client.responses.create(
            model=self.MODEL,
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        text = response.output_text

        if not text or not text.strip():
            raise InterpreterError("Model returned an empty response.")

        return text

    def _parse_json(self, text: str) -> dict:
        text = text.strip()

        if text.startswith("```"):
            text = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                text,
                flags=re.MULTILINE
            ).strip()

        return json.loads(text)

    def _apply_defaults(self, data: dict) -> dict:
        defaults = asdict(Command())
        defaults.update(data)
        return defaults