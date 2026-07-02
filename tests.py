from functions.get_files_info import get_files_info

def main():
    root_content = get_files_info("calculator")
    print(root_content)

    pkg_content = get_files_info("calculator", "pkg")
    print(pkg_content)

    pkg_content = get_files_info("calculator", "../")
    print(pkg_content)

    pkg_content = get_files_info("calculator", "/bin")
    print(pkg_content)

main()