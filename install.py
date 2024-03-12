import os
import sys
from pathlib import Path

# Get the directory where the install.py script is located
install_dir = Path(__file__).parent.absolute()

# Define the path for the combiner.bat file
bat_file_path = install_dir / 'combine.bat'

# Batch file contents
bat_contents = """
@echo off
python "{}" %*
""".format(install_dir / 'main.py')

# Write the contents to combiner.bat
with open(bat_file_path, 'w') as bat_file:
    bat_file.write(bat_contents)

# Function to add the directory to the PATH environment variable
def add_to_path(directory):
    # Get the current PATH variable
    current_path = os.environ.get('PATH', '')

    # Check if the directory is already in PATH
    if str(directory) not in current_path:
        # Add the directory to PATH
        os.environ['PATH'] += os.pathsep + str(directory)

        # Depending on the OS, update the PATH variable persistently
        if sys.platform == 'win32':
            # Add to the user's PATH
            os.system(f'setx PATH "%PATH%;{directory}"')

print(f"Adding {install_dir} to PATH...")
add_to_path(install_dir)

print("Installation complete. You can now use 'combiner.bat' from the terminal.")
