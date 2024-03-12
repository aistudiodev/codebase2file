# Dir2TXT

Dir2TXT is a utility for merging code files within a directory into a single text file.

**Examples:**

Merge files in the current directory:

```bash
combine .
```

Merge files in the `src` directory, including only Python and JavaScript files. Save as `merged.txt`:

```bash
combine src -o merged.txt -e py,js
```

## Installation

To get the tool on your system, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/aistudiodev/dir2txt.git
```

2. Navigate to the directory:

```bash
cd dir2txt
```

3. Run the script:

```bash
python main.py <directory> [options]
```

## Make it available in the terminal (Windows only)

> For other operating systems, feel free to modify the installation script to suit your OS.

Run the installation script:

```bash
python install.py
```

This adds the `combine` command to your terminal. Restart your terminal for the changes to take effect.

## Arguments and Options

### Usage:

```bash
combine <directory> [options]
```

### Arguments:

- `directory`: The directory to process. Use `.` to indicate the current directory.

### Options:

- `-o`, `--output`: (Optional) The path to the output file. If not specified, the output file will be named after the processed directory with a `.txt` extension and saved within the same directory.
- `-e`, `--extensions`: (Optional) A comma-separated list of file extensions to include (without the dot). For example, `py,js,html`.

## Notes

- The tool automatically excludes files and directories specified in .gitignore and the .git directory.

## Troubleshooting

If you encounter issues, please create an issue on the GitHub repository.
