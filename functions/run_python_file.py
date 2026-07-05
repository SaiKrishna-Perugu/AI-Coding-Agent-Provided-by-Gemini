import os
import subprocess
from google.genai import types

def is_within_directory(directory, path):
    """Check if a path is within a directory."""
    abs_path = os.path.abspath(path)
    abs_directory = os.path.abspath(directory)
    return abs_path.startswith(abs_directory)

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not is_within_directory(abs_working_directory, abs_file_path):
        return f'Cannot execute "{file_path}" as it is outside'
    if not os.path.isfile(abs_file_path):
        return f'"{file_path}" does not exist'
    if not file_path.endswith(".py"):
        return f'"{file_path}" is not a Python file'

    try:
        final_args = ["python3", file_path]
        if args:
            final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_directory,
            timeout=30, capture_output=True, text=True
        )
        final_string =  f""" 
        
        STDOUT: {output.stdout}
        STDERR: {output.stderr}
        """

        if output.returncode != 0:
            return f"Process exited with code {output.returncode}"
        if output.stdout == "" and output.stderr == "":
            return "No output from the Python file."
        return final_string
    except Exception as e:
        return  f"Error: executing Pytho file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file with the python3 interpreter and optional CLI arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional array of string CLI arguments for the Python file",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },
        # required=["file_path"],
    ),
)