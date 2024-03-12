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

def is_ignored(file_path, patterns, root, output_file, extensions):
    relative_path = os.path.relpath(file_path, root)
    if os.path.abspath(file_path) == os.path.abspath(output_file):
        return True
    _, file_extension = os.path.splitext(file_path)
    if extensions and file_extension[1:] not in extensions:
        return True
    for pattern in patterns:
        if pattern.startswith('/'):
            pattern = pattern[1:]
        if pattern.endswith('/'):
            pattern = pattern[:-1]
        if fnmatch.fnmatch(file_path, os.path.join(root, pattern)) or fnmatch.fnmatch(relative_path, pattern):
            return True
        if os.path.isdir(file_path) and fnmatch.fnmatch(file_path, os.path.join(root, pattern + '/*')):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in relative_path.split(os.sep)):
            return True
    return False

def process_directory(directory, output_file, extensions):
    patterns = read_gitignore(directory)
    patterns.append('.git/')  # Skip .git folder files
    skipped_node_modules = False

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            if '.git' in dirs:
                dirs.remove('.git')  # Skip .git folder during traversal

            for file in files:
                file_path = os.path.join(root, file)
                if is_ignored(file_path, patterns, directory, output_file, extensions):
                    if 'node_modules' in file_path:
                        skipped_node_modules = True
                    continue

                # Write header with file information
                outfile.write(f"=== {file_path} ===\n")

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n")  # Add a separator between files
                except UnicodeDecodeError:
                    print(f"Skipping file: {file_path} (Unicode decode error)")
                except Exception as e:
                    print(f"Error processing file: {file_path} ({str(e)})")

            # Update the animated text
            sys.stdout.write(f"\rMerging into {output_file}{'.' * (int(time.time()) % 4)}")
            sys.stdout.flush()

    if skipped_node_modules:
        print("\nSkipped node_modules folder.")

def main():
    parser = argparse.ArgumentParser(description='Combine code files into a continuous text file.')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('-e', '--extensions', help='Comma-separated list of file extensions to include (without the dot)', default='')
    args = parser.parse_args()

    extensions = args.extensions.split(',') if args.extensions else []

    process_directory(args.directory, args.output, extensions)
    print(f"\nCode files combined into: {args.output}")

if __name__ == '__main__':
    main()