# Brainfuck Compiler

Python script that compiles brainfuck to C, alongside bash scripts to make life easier

## Requirements

- Python 3.12
- gcc
- clang-formatter
- A good OS (not Windows)

## Usage

You can use main.py directly

```bash
python3 main.py [FILE] # Output to terminal
python3 main.py [FILE] -o [FILE] # Output to FILE
```

Or you can move the desired .bf file to `src` run `bash ./compile.sh` and `bash ./run.sh` and select the binary.

## License

The bash scripts have MIT License

The bf code without attributtion are CC0 (Taken from esolang wiki)

The bf code with attributtion to Daniel B. Cristofani are Attribution-ShareAlike 4.0 International
