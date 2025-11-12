import os
import sys


def write_to_appdata(relative_path, data):
    # Get the path to the Roaming AppData directory
    appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

    # Create the full path for the specified subdirectory and file
    full_path = os.path.join(appdata_path, relative_path)

    # Check if the file exists
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        print('Missing files and directories will be restored')

    # Extract the directory part of the full path
    directory = os.path.dirname(full_path)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Write to the file
    with open(full_path, 'w') as f:
        f.write(data)

    print(f"Data written to: {full_path}")


def read_from_appdata(relative_path):
    # Get the path to the Roaming AppData directory
    appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

    # Create the full path for the specified subdirectory and file
    full_path = os.path.join(appdata_path, relative_path)

    # Check if the file exists
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        print('Missing files and directories will be restored')
        return None

    # Read the file
    with open(full_path, 'r') as f:
        data = f.read()

    print(f"Data read from: {full_path}")
    return data


# For reading embedded files
# def resource_path(relative_path):
#     """ Get the absolute path to the resource (for both exe and dev modes) """
#     try:
#         # If the application is running as a PyInstaller executable
#         base_path = sys._MEIPASS
#     except AttributeError:
#         # If running in development mode
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)

def resource_path(relative_path):
    """ Get the absolute path to the resource (for both exe and dev modes) """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in development mode, get the folder of the main script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)