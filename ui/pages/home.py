from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from common_fn import cutie_label_style, boldie_label_style

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        layout.addWidget(continue_watching_title)

        layout.addStretch()
