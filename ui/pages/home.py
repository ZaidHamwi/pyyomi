from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from common_fn import cutie_label_style, boldie_label_style, resource_path, ScrollWidget

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Continue watching
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        layout.addWidget(continue_watching_title)



        continue_wdg = ScrollWidget()
        layout.addWidget(continue_wdg)

        layout.addStretch()

        # DEMO
        for i in range(10):
            continue_wdg.add_image(resource_path("embedded_images/demo.jpg"))
