import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(MAX_CHARS)
            truncated = len(content) >= MAX_CHARS

        header = f'{file_path} truncated: {truncated}'
        return f'{header}\n{content}'
    
    except Exception as e:
        return f'Error: Exception reading file: {e}'
