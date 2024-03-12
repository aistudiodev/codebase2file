# Dir2TXT

This is a utility for merging all code files within a given directory into a single text file. It is particularly useful for creating a large, contiguous text file from a codebase, which can then be processed or analyzed further.

## Usage Examples

Merge files in the current directory, with output named after the directory:

```bash
combine .
```

Merge files in the `src` directory, including only Python and JavaScript files, and specify the output file:

```bash
combine src -o merged.txt -e py,js
```

## Installation (Windows specific)

> **NOTE:** This tool is currently designed for use on Windows systems. For other operating systems, you can run the `main.py` script directly.

To install the tool, follow these steps:

1. Clone the repository or download the source files to your local machine.

```bash
git clone https://github.com/aistudiodev/dir2txt.git
```

2. Navigate to the directory containing the `install.py` script in the terminal.

```bash
cd dir2txt
```

3. Run the installation script with Python:

```bash
python install.py
```

This will create a `combine.bat` file and add the tool's directory to your system's PATH, making the `combine` command available in your terminal.

**IMPORTANT:** You may need to restart your terminal for the changes to take effect.

## Arguments and Options

To use the tool, navigate to the directory you want to process or provide the path to the directory as an argument. Use the following command:

```bash
combine <directory> [options]
```

### Arguments:

- `directory`: The directory to process. Use `.` to indicate the current directory.

### Options:

- `-o`, `--output`: (Optional) The path to the output file. If not specified, the output file will be named after the processed directory with a `.txt` extension and saved within the same directory.
- `-e`, `--extensions`: (Optional) A comma-separated list of file extensions to include (without the dot). For example, `py,js,html`.

## Notes

- The tool will automatically read `.gitignore` and exclude these files and directories.
- It also excludes files in the hidden `.git` directory.

## Troubleshooting

If you encounter issues running the tool, feel free to reach out or create an issue on the GitHub repository.
