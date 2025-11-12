import sys
import os
from PySide6 import QtWidgets
from ui_main import App

if __name__ == '__main__':
    print(__name__)
    app = QtWidgets.QApplication(sys.argv)
    launcher = App()
    launcher.show()
    sys.exit(app.exec())