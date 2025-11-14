from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt
from common_fn import cutie_label_style, resource_path, ScrollWidget


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # OUTER LAYOUT (only holds the scroll area)
        outer_layout = QVBoxLayout(self)

        # SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        outer_layout.addWidget(scroll)

        # INNER CONTENT WIDGET (the actual page)
        content = QWidget()
        scroll.setWidget(content)

        # INNER LAYOUT (where you add your page content)
        layout = QVBoxLayout(content)


        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        layout.addWidget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg = ScrollWidget()
        layout.addWidget(continue_wdg)

        layout.addStretch()


        # DEMO IMAGES
        for i in range(20):
            continue_wdg.add_image(resource_path("embedded_images/demo.jpg"))
