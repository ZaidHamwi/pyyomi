import sys
import os
import qtawesome
from PySide6.QtWidgets import QStackedWidget, QFrame
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from common_fn import read_from_appdata, write_to_appdata, resource_path

from ui.pages.home import HomePage
from ui.pages.settings import SettingsPage

from ui.ui_sidebar import Sidebar


class App(QtWidgets.QMainWindow):

    # Initialise App
    def __init__(self):
        super().__init__()

        # Main Widget and Layout
        self.main_wdg = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.main_wdg)

        self.app_folder = 'pyyomi'  # Name of appdata folder

        # Settings list NEEDS TO BECOME JSON AND BETTER THAN THIS!!!
        # self.settings = ['']

        # App UI Elements here:


        self.init_ui()
        self.populate_ui()
        self.connect_signals()

    # Initialise UI
    def init_ui(self):
        self.setWindowTitle(' Pyyomi')
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self.setWindowIcon(QIcon(resource_path("embedded_images/app_icon.ico")))

        # Read Settings File NEEDS TO BECOME JSON AND BETTER THAN THIS!!!
        #
        # settings_data = read_from_appdata(f'{self.app_folder}/config/app_settings.txt')
        #
        # if settings_data is not None:
        #     self.settings = settings_data.splitlines()
        #     print('Settings: ' + str(self.settings))
        #
        # if not settings_data:
        #     # Makes new settings file
        #     print('Overwriting settings file...')
        #
        #     settings_data = '\n'.join(self.settings)
        #     print(f'''Writing these settings:
        #
        #             {settings_data}''')
        #     write_to_appdata(f'{self.app_folder}/config/app_settings.txt', settings_data)

        # MAIN Widget

        self.setCentralWidget(self.main_wdg)

        # MAIN Layout
        self.main_wdg.setLayout(self.layout)

        # SIDEBAR
        self.sidebar = Sidebar()
        self.layout.addWidget(self.sidebar)
        self.sidebar.setFixedWidth(150)

        # Vertical QFrame
        v_line = QtWidgets.QFrame()
        v_line.setFrameShape(QFrame.VLine)
        v_line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(v_line)

        # STACK
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack, 1)
        # Add pages
        self.pages = {
            "home": HomePage(),
            "settings": SettingsPage()
        }
        for page in self.pages.values():
            self.stack.addWidget(page)


    def populate_ui(self):
        print('Populated UI.')

    def connect_signals(self):
        print('Connecting signals...')
        self.sidebar.page_selected.connect(self.switch_page)

    def switch_page(self, name):
        page = self.pages.get(name)
        if page:
            self.stack.setCurrentWidget(page)


if __name__ == '__main__':
    print(__name__)
    app = QtWidgets.QApplication(sys.argv)
    launcher = App()
    launcher.show()
    sys.exit(app.exec())

