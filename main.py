import sys
import os
from PySide6 import QtWidgets
from ui_main import App


app = QtWidgets.QApplication(sys.argv)
launcher = App()
launcher.show()
sys.exit(app.exec())