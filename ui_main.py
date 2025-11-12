import sys
import os
import qtawesome
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon


class App(QtWidgets.QMainWindow):

    # Initialise App
    def __init__(self):
        super().__init__()

        # Main Widget and Layout
        self.main_wdg = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.main_wdg)

        self.app_folder = 'pyyomi'  # Name of appdata folder

        # Settings list
        self.settings = ['']

        # App UI Elements here:


        self.init_ui()
        self.populate_ui()
        self.connect_signals()

    # Initialise UI
    def init_ui(self):
        self.setWindowTitle(' Pyyomi')
        self.setWindowIcon(QIcon('embedded_images/app_icon.ico'))

        # Read Settings File
        settings_data = self.read_from_appdata(f'{self.app_folder}/config/app_settings.txt')

        if settings_data is not None:
            self.settings = settings_data.splitlines()
            print('Settings: ' + str(self.settings))

        if not settings_data:
            # Makes new settings file
            print('Overwriting settings file...')

            settings_data = '\n'.join(self.settings)
            print(f'''Writing these settings:

                    {settings_data}''')
            self.write_to_appdata(f'{self.app_folder}/config/app_settings.txt', settings_data)

        # MAIN Widget
        self.setCentralWidget(self.main_wdg)

        # MAIN Layout
        self.main_wdg.setLayout(self.layout)

    def populate_ui(self):
        print('Populated UI.')

    def connect_signals(self):
        print('Connecting signals...')

    def write_to_appdata(self, relative_path, data):
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

    def read_from_appdata(self, relative_path):
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
    def resource_path(self, relative_path):
        """ Get the absolute path to the resource (for both exe and dev modes) """
        try:
            # If the application is running as a PyInstaller executable
            base_path = sys._MEIPASS
        except AttributeError:
            # If running in development mode
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    print(__name__)
    app = QtWidgets.QApplication(sys.argv)
    launcher = App()
    launcher.show()
    sys.exit(app.exec())

