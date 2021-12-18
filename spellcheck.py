import subprocess
import pathlib
import knownwords

def get_files_to_check():
    for path in pathlib.Path("documenti").glob("**/*.tex"):
        yield path

def check_file(file):
    exit_code = 0

    content = file.read_text()

    aspell_out = subprocess.check_output(
        ["aspell", "-t", "--list", "--lang=it"], 
        input = content,
        text = True
    )

    incorrect_words = set(aspell_out.split("\n")) \
                      - {""} \
                      - knownwords.words

    if len(incorrect_words) > 0:
        print(f"In {file} the following words are not known: ")
        for string in sorted(incorrect_words):
            print(string)
        exit_code = 1

    return exit_code

def check_files():
    exit_code = 0
    for file in get_files_to_check():
        exit_code += check_file(file)

    return 1 if exit_code > 0 else 0

exit(check_files())

