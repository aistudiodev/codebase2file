import os
import argparse
import fnmatch
import time
import sys

def read_gitignore(directory):
    gitignore_path = os.path.join(directory, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as file:
            for line in file:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    patterns.append(stripped)
    return patterns

def is_ignored(path, patterns, root, output_file, extensions):
    # Check if the path is the output file itself
    if os.path.abspath(path) == os.path.abspath(output_file):
        return True
    # Check if the path matches any of the patterns
    for pattern in patterns:
        if pattern.startswith('/'):
            pattern = pattern[1:]
        if pattern.endswith('/'):
            pattern = pattern[:-1]
        if fnmatch.fnmatch(path, os.path.join(root, pattern)) or fnmatch.fnmatch(os.path.relpath(path, root), pattern):
            return True
        if os.path.isdir(path) and fnmatch.fnmatch(path, os.path.join(root, pattern + '/*')):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in os.path.relpath(path, root).split(os.sep)):
            return True
    # Check if the file extension is not in the list of extensions to include
    if os.path.isfile(path):
        _, file_extension = os.path.splitext(path)
        if extensions and file_extension[1:].lower() not in extensions:
            return True
    return False

def process_directory(directory, output_file, extensions):
    patterns = read_gitignore(directory)
    patterns.append('.git/')  # Skip .git folder files

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            # Remove ignored directories from dirs
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), patterns, directory, output_file, extensions)]

            for file in files:
                file_path = os.path.join(root, file)
                if is_ignored(file_path, patterns, directory, output_file, extensions):
                    continue

                # Get the relative path to the input directory
                relative_path = os.path.relpath(file_path, directory)

                # Write header with file information
                outfile.write(f"=== {relative_path} ===\n")

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n")  # Add a separator between files
                except UnicodeDecodeError:
                    print(f"Skipping file: {relative_path} (Unicode decode error)")
                except Exception as e:
                    print(f"Error processing file: {relative_path} ({str(e)})")

            # Update the animated text
            sys.stdout.write(f"\rMerging into {os.path.basename(output_file)}{'.' * (int(time.time()) % 4)}")
            sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description='Combine code files into a continuous text file.')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('-o', '--output', help='Optional: Output file path', nargs='?', default=None)
    parser.add_argument('-e', '--extensions', help='Comma-separated list of file extensions to include', default='')
    args = parser.parse_args()

    extensions = [ext.lower() for ext in args.extensions.split(',')] if args.extensions else []

    # Resolve the actual path of the directory
    directory_path = os.path.realpath(args.directory)

    # If no output is provided, create one based on the directory name
    if args.output:
        output_file = os.path.realpath(args.output)
    else:
        # Get the name of the last directory in the path
        directory_name = os.path.basename(os.path.normpath(directory_path))
        # Construct the output file path using the directory name and appending '.txt'
        output_file = os.path.join(directory_path, '..', f"{directory_name}.txt")

    # Ensure the output file path is absolute
    output_file = os.path.abspath(output_file)

    process_directory(directory_path, output_file, extensions)
    print(f"\nFiles combined into: {output_file}")

if __name__ == '__main__':
    main()