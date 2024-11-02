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

def group_repeated_chars(s):
    """Returns a list of the commands but same commands are grouped
        "+++>++<-"
        "+++", ">", "++", "<", "-"
    """
    return [''.join(group) for _, group in groupby(s)]

def command_to_c(s: str):
    """Given a string of one or more repeated commands, return a line of C code."""
    command = s[0]
    number = len(s)

    match command:
        case '<':
            return f"ptr -= {number};"  # Move pointer to the left
        case '>':
            return f"ptr += {number};"  # Move pointer to the right
        case '+':
            return f"*ptr += {number};"  # Increment value at the pointer
        case '-':
            return f"*ptr -= {number};"  # Decrement value at the pointer
        case '.':
            return "putchar(*ptr);"*number  # Output the value at the pointer
        case ',':
            return "*ptr = getchar();"*number  # Input value into the pointer
        case '[':
            return "while (*ptr) {"*number  # Begin loop
        case ']':
            return "}"*number  # End loop
        case _:
            return ""  # Default case for any unsupported command

def brainfuck_to_c(brainfuck_code):
    listed_code = group_repeated_chars(brainfuck_code)

    c_code = []

    # Initialize C code structure
    c_code.append("#include <stdio.h>")
    c_code.append("int main() {")
    c_code.append("unsigned char memory[30000] = {0};")
    c_code.append("unsigned char *ptr = memory;")

    # Parse Brainfuck code
    for command in listed_code:
        c_code.append(command_to_c(command))

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

def debug(string: str, verbose: bool):
    if verbose:
        click.echo(f"DEBUG: {string}")


def save_c_code(code, file:str):
    if not file.endswith(".c"):
        file += ".c"
    with open(file, "w") as f:
        f.write(code)

@click.command()
@click.argument("file")
@click.option("--output", "-o", required=False, help="Output of C file")
@click.option("--verbose", "-v", is_flag=True, help="Debug code")
def main(file: str, output: str, verbose: bool):

    if not output.endswith(".c"):
        output += ".c"

    input_code = get_code(file)

    debug(f"RAW CODE\n{input_code}", verbose)

    code = clean_code(input_code)

    debug(f"CLEAN CODE\n{code}", verbose)

    c_code = brainfuck_to_c(code)

    c_code = format_c_code(c_code)

    debug(f"Formatted C Code: {c_code}", verbose)

    if output:
        debug(f"File will be written to {output}", verbose)
        save_c_code(c_code, output)

if __name__ == "__main__":
    main()
