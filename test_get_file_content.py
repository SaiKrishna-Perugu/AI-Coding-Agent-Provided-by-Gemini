from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def main():
    working_directory = "calculator"
    print(get_file_content(working_directory, "lorem.txt"))
    print(get_file_content(working_directory, "pkg/calculator.py"))
    print(get_file_content(working_directory, "main.py"))
    print(get_file_content(working_directory, "/bin/cat"))
    print(get_file_content(working_directory, "pkg/does_not_exist.py"))

main()