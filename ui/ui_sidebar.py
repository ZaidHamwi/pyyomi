from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    page_selected = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        buttons = {
            "Home": "home",
            "Anime": "settings",
            "Movies": "settings",
            "Shows": "settings",
            "Manga": "settings",
            "Manhwa": "settings",
            "Light Novels": "settings",
            "e-Books": "settings",
            "Watched": "settings",
            "Want to Watch": "settings",
            "Dropped": "settings",
            "Settings": "settings"
        }

        # group ensures only ONE is checked at a time
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

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
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:checked {
                background-color: #3a3a3a;
            }
        """)

        # store button references
        self.button_map = {}

        for label, name in buttons.items():
            btn = QPushButton(label)
            btn.setCheckable(True)    # <--- IMPORTANT
            btn.clicked.connect(lambda checked, n=name: self.select_page(n))
            layout.addWidget(btn)

            self.btn_group.addButton(btn)
            self.button_map[name] = btn

        layout.addStretch()

        # Default selected page
        self.select_page("home")

    def select_page(self, name: str):
        """Highlight the selected button + emit signal."""
        # check the correct button
        btn = self.button_map[name]
        btn.setChecked(True)

        # emit page name
        self.page_selected.emit(name)
