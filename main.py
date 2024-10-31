import click
import subprocess
import tempfile
import os
from itertools import groupby

BF_CHARS = "><+-.,[]"


def get_code(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


def clean_code(code: str) -> str:
    """Removes any charachter that is not brainfuck code"""
    return "".join(c for c in code if c in BF_CHARS)


def brainfuck_to_c(brainfuck_code):
    # Define command mappings
    command_map = {
        '>': "++ptr;",               # Move pointer to the right
        '<': "--ptr;",               # Move pointer to the left
        '+': "++*ptr;",              # Increment value at the pointer
        '-': "--*ptr;",              # Decrement value at the pointer
        '.': "putchar(*ptr);",       # Output the value at the pointer
        ',': "*ptr = getchar();",    # Input value into the pointer
        '[': "while (*ptr) {",       # Begin loop
        ']': "}"                     # End loop
    }

    c_code = []

    # Initialize C code structure
    c_code.append("#include <stdio.h>")
    c_code.append("int main() {")
    c_code.append("unsigned char memory[30000] = {0};")
    c_code.append("unsigned char *ptr = memory;")

    # Parse Brainfuck code
    for command in brainfuck_code:
        if command in command_map:
            c_code.append(command_map[command] + "\n")  # Append the corresponding C code

    # Close the main function
    c_code.append("return 0;")
    c_code.append("}")

    return "\n".join(c_code)

def format_c_code(c_code):
    # Create a temporary file to hold the C code
    with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_file:
        temp_file.write(c_code.encode())
        temp_file_path = temp_file.name

    # Use clang-format to format the C code
    formatted_code = subprocess.check_output([
        "clang-format",
        "-style",
        "{IndentWidth: 4}",
        temp_file_path,
    ]).decode()

    # Clean up the temporary file
    os.remove(temp_file_path)

    return formatted_code


def save_c_code(code, file:str):
    if not file.endswith(".c"):
        file += ".c"
    with open(file, "w") as f:
        f.write(code)

@click.command()
@click.argument("file")
@click.option("--output", "-o", required=False, help="Output of C file")
def main(file: str, output: str):

    if not output.endswith(".c"):
        output += ".c"

    input_code = get_code(file)

    code = clean_code(input_code)

    c_code = brainfuck_to_c(code)

    c_code = format_c_code(c_code)

    click.echo(c_code)

    if output:
        save_c_code(c_code, output)

if __name__ == "__main__":
    main()
