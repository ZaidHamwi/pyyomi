from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QPushButton, QHBoxLayout

from common_fn import title_label_style, VScrollWidget, bold_label_style, CollapsibleWidget


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


        # SETTING TILES
        data_and_storage = CollapsibleWidget("Data and storage")
        data_and_storage.addWidget(QLabel("Storage location:"))
        data_and_storage.addWidget(QLabel("Library size:"))
        data_and_storage.addWidget(QLabel("Disk space:"))
        data_and_storage.addWidget(QLabel("Automatic backup frequency:"))
        backup_buttons_wdg = QWidget()
        backup_buttons_layout = QHBoxLayout(backup_buttons_wdg)
        backup_buttons_layout.addWidget(QPushButton("Create backup"))
        backup_buttons_layout.addWidget(QPushButton("Restore backup"))
        data_and_storage.addWidget(backup_buttons_wdg)

        collapsible2 = CollapsibleWidget("Preferences")
        collapsible2.addWidget(QPushButton("Enable Notifications"))
        collapsible2.addWidget(QPushButton("Change Theme"))


        settings_wdg = VScrollWidget()
        outer_layout.addWidget(settings_wdg)

        settings_wdg.addSpacer(10, 10)

        settings_wdg.addWidget(data_and_storage)
        settings_wdg.addWidget(collapsible2)


        settings_wdg.addStretch()
