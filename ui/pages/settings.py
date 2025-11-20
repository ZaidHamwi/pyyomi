from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame

from common_fn import title_label_style, VScrollWidget, bold_label_style, HScrollWidget


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        # OUTER LAYOUT (only holds the scroll area)
        outer_layout = QVBoxLayout(self)

        # Settings title
        settings_title = QLabel("Settings")
        settings_title.setStyleSheet(title_label_style)
        outer_layout.addWidget(settings_title)

        top_divider = QFrame()
        top_divider.setFrameShape(QFrame.HLine)
        top_divider.setFrameShadow(QFrame.Sunken)
        outer_layout.addWidget(top_divider)

        settings_wdg = VScrollWidget()
        outer_layout.addWidget(settings_wdg)



        settings_wdg.add_stretch()
