import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import errors as google_errors
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt> [--verbose]")
        sys.exit(1)

    verbose_flag = "--verbose" in sys.argv[2:]

    prompt = sys.argv[1]
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=system_prompt + "\n\nUser request: " + prompt)],
        )
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages[0],
            config=config,
        )
    except google_errors.ClientError as exc:
        if verbose_flag:
            raise

        status_code = getattr(exc, "status_code", None)
        response_json = getattr(exc, "response_json", None)
        message = str(exc)

        if status_code == 429 or "RESOURCE_EXHAUSTED" in message:
            print("Gemini API quota exceeded. Please wait a few minutes and try again, or use a different API key/plan.")
        else:
            print(f"Gemini API request failed: {message}")

        if response_json:
            print(f"Details: {response_json}")
        sys.exit(1)

    if verbose_flag:
        print(f"Response object: {response}")

    if hasattr(response, "text") and response.text:
        print(response.text)
    else:
        print(response)


if __name__ == "__main__":
    main()