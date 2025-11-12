import sys
import os
import qtawesome
from common_fn import read_from_appdata, write_to_appdata, resource_path
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
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setWindowIcon(QIcon('embedded_images/app_icon.ico'))

        # Read Settings File
        settings_data = read_from_appdata(f'{self.app_folder}/config/app_settings.txt')

        if settings_data is not None:
            self.settings = settings_data.splitlines()
            print('Settings: ' + str(self.settings))

        if not settings_data:
            # Makes new settings file
            print('Overwriting settings file...')

            settings_data = '\n'.join(self.settings)
            print(f'''Writing these settings:

                    {settings_data}''')
            write_to_appdata(f'{self.app_folder}/config/app_settings.txt', settings_data)

        # MAIN Widget
        self.setCentralWidget(self.main_wdg)

        # MAIN Layout
        self.main_wdg.setLayout(self.layout)

    def populate_ui(self):
        print('Populated UI.')

    def connect_signals(self):
        print('Connecting signals...')


if __name__ == '__main__':
    print(__name__)
    app = QtWidgets.QApplication(sys.argv)
    launcher = App()
    launcher.show()
    sys.exit(app.exec())

