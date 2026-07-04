import os

def is_within_directory(directory, path):
    """Check if a path is within a directory."""
    abs_directory = os.path.abspath(directory)
    abs_path = os.path.abspath(path)
    return abs_path.startswith(abs_directory)

def write_file(working_directory: str, file_path: str, content: str) -> str:

    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: "{file_path}" is not a working directory'
    
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Could not create parent dirs: {parent_dir} = {e}'
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (f'Successfully wrote to "{file_path} ({len(content)} characters written)')
    except Exception as e:
        return f'Failed to write to file: {file_path}, {e}'
