from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt
from common_fn import title_label_style, resource_path, HScrollWidget, VScrollWidget, \
    bold_label_style


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # OUTER LAYOUT (only holds the scroll area)
        outer_layout = QVBoxLayout(self)

        # Home title
        home_title = QLabel("Home")
        home_title.setStyleSheet(title_label_style)
        outer_layout.addWidget(home_title)

        top_divider = QFrame()
        top_divider.setFrameShape(QFrame.HLine)
        top_divider.setFrameShadow(QFrame.Sunken)
        outer_layout.addWidget(top_divider)

        home_wdg = VScrollWidget()
        outer_layout.addWidget(home_wdg)



        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(bold_label_style)
        home_wdg.addWidget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg = HScrollWidget()
        home_wdg.addWidget(continue_wdg)

        home_wdg.addStretch()

        # DEMO IMAGES
        for i in range(10):
            continue_wdg.addImage(resource_path("embedded_images/demo.jpg"))

        continue_wdg.addStretch()
