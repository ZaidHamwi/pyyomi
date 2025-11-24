from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QPushButton

from common_fn import title_label_style, VScrollWidget, bold_label_style, HScrollWidget, CollapsibleWidget


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

        collapsible = CollapsibleWidget("Pet Details")
        collapsible.addWidget(QLabel("Name: PIKA"))
        collapsible.addWidget(QLabel("Age: 5"))
        collapsible.addWidget(QPushButton("Edit Profile"))

        collapsible2 = CollapsibleWidget("Preferences")
        collapsible2.addWidget(QPushButton("Enable Notifications"))
        collapsible2.addWidget(QPushButton("Change Theme"))


        settings_wdg = VScrollWidget()
        outer_layout.addWidget(settings_wdg)

        settings_wdg.addWidget(collapsible)
        settings_wdg.addWidget(collapsible2)


        settings_wdg.addStretch()
