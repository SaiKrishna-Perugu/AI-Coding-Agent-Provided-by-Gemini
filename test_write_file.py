from functions.write_file import write_file

def main():
    working_directory = "calculator"
    print(write_file(working_directory, "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file(working_directory, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file(working_directory, "/tmp/temp.txt", "this should not be allowed"))

main()