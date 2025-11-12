from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

# demo
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Welcome to Pyomi Home!"))
