from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    page_selected = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        buttons = {
            "Home": "home",
            "Settings": "settings"
        }


        # Style, NEEDS FIXING
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            QPushButton {
                color: white;
                background-color: transparent;
                border: none;
                padding: 10px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:checked {
                background-color: #333;
                font-weight: bold;
            }
        """)

        for label, name in buttons.items():
            btn = QPushButton(label)
            btn.setStyleSheet("padding: 12px; color: white; text-align: left;")
            btn.clicked.connect(lambda checked, n=name: self.page_selected.emit(n))
            layout.addWidget(btn)

        layout.addStretch()
