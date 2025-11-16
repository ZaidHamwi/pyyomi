from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal

from common_fn import VScrollWidget   # <-- your reusable scroll widget


class Sidebar(QWidget):
    page_selected = Signal(str)

    def __init__(self):
        super().__init__()

        # ---- outer layout ----
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # ---- replace direct layout with your scroll widget ----
        self.scroll_area = VScrollWidget(
            item_spacing=0,
            h_scroll_bar=False,
            v_scroll_bar=False,
            container_name="sidebar_container"
        )
        layout.addWidget(self.scroll_area)  # sidebar is now scrollable
        self.scroll_area.add_spacer(10, 10)

        # -----------------------------------------
        # BUTTON LIST
        # -----------------------------------------
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

        # ---- exclusive checked behavior ----
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        # ---- styles ----
        self.setStyleSheet("""
            QWidget#sidebar_container {
                background-color: #1a1a1a;
                border-radius: 4px;
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
                border-radius: 8px;
            }

            QPushButton:checked {
                background-color: #3a3a3a;
                border-radius: 8px;
            }
        """)

        self.button_map = {}

        # -----------------------------------------
        # ADD BUTTONS INTO THE SCROLLING LAYOUT
        # -----------------------------------------
        for label, name in buttons.items():
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.select_page(n))

            self.scroll_area.add_widget(btn)
            self.btn_group.addButton(btn)
            self.button_map[name] = btn

        self.scroll_area.add_spacer(10, 10)

        self.scroll_area.add_stretch()

        # default selection
        self.select_page("home")

    # -----------------------------------------
    # highlight + emit page name
    # -----------------------------------------
    def select_page(self, name: str):
        btn = self.button_map[name]
        btn.setChecked(True)
        self.page_selected.emit(name)
