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
            "Anime": "settings2",
            "Movies": "settings3",
            "Shows": "settings4",
            "Manga": "settings5",
            "Manhwa": "settings6",
            "Light Novels": "settings7",
            "e-Books": "settings8",
            "Watched": "settings9",
            "Want to Watch": "settings10",
            "Dropped": "settings11",
            "1": "settings12",
            "2": "settings13",
            "3": "settings14",
            "4": "settings15",
            "5": "settings16",
            "6": "settings17",
            "7": "settings18",
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

        # --- Compute minimum height ---
        total_height = 0
        for btn in self.button_map.values():
            total_height += btn.sizeHint().height()
        print(total_height)

        # add layout spacing between buttons
        spacing = self.layout().spacing()
        total_height += spacing * (len(self.button_map) - 1)

        self.setMinimumHeight(total_height)

        # Default selected page
        self.select_page("home")

    def select_page(self, name: str):
        """Highlight the selected button + emit signal."""
        # check the correct button
        btn = self.button_map[name]
        btn.setChecked(True)

        # emit page name
        self.page_selected.emit(name)
