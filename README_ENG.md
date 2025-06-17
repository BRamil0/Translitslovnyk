# Translitslovnyk

__[Українська](README.md)__

#### Description
Translitslovnyk is a console application for transliterating text using dictionaries.

### Features
- Support for multiple transliteration dictionaries.
- Interactive mode and file processing capabilities.
- Automatic Unicode normalization for correct handling of diacritics.
- Intelligent case handling for characters.
- A pleasant and informative console interface (powered by Rich).
- Multilingual interface support.
- Command-line argument support for processing text files.
- Support for user interface localization.

### Installation
1.  Download Python 3.13 or a newer version.
2.  Clone the repository:
    ```bash
    git clone https://github.com/BRamil0/Translitslovnyk.git
    ```
3.  Navigate to the project directory.
4.  Create a virtual environment and install the dependencies:
    ```bash
    python -m venv venv
    pip install -r requirements.txt
    ```
    If you have [uv](https://github.com/astral-sh/uv) installed:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```
5.  Compile the files (requires a C compiler, Optional):
    ```bash
    nuitka --standalone --onefile --windows-console-mode=force --output-filename=ts main.py
    ```
    You can also use the following parameters:
    - `--lto=no` — To disable LTO.
    - `--clang` — To use the Clang compiler.

### Usage
Simply type in your console (if you've added the binary to your PATH):
```bash
ts [arguments]
```
Or run it via Python:
```bash
python main.py [arguments]
```
#### Arguments
All arguments are optional. If you don't specify an input file or text, the program will prompt you for them in the console.
-   `-i`, `--input` — Specify the input file for transliteration.
-   `-o`, `--output` — Specify the output file to save the result. Requires the dictionary and input file to be explicitly provided via arguments.
-   `-d`, `--dictionary` — Specify the dictionary for transliteration.
-   `-t`, `--text` — Specify the text for transliteration.
-   `-h`, `--help` — Show the help message.
-   `-v`, `--version` — Show the program version.
-   `-l`, `--language` — Specify the program's language. If not provided, Ukrainian will be used.

These are the main arguments. All other arguments can be viewed in the program's help message.

### License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.