from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt
from common_fn import cutie_label_style, resource_path, HScrollWidget, SmoothScrollMixin, VScrollWidget


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # OUTER LAYOUT (only holds the scroll area)
        outer_layout = QVBoxLayout(self)

        # # SCROLL AREA
        # scroll = QScrollArea()
        # scroll.setWidgetResizable(True)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scroll.setFrameShape(QFrame.NoFrame)
        #
        # outer_layout.addWidget(scroll)
        #
        # # INNER CONTENT WIDGET (the actual page)
        # content = QWidget()
        # scroll.setWidget(content)
        #
        # # INNER LAYOUT (where you add your page content)
        # layout = QVBoxLayout(content)

        home_wdg = VScrollWidget(v_scroll_bar=True)
        outer_layout.addWidget(home_wdg)


        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg = HScrollWidget()
        home_wdg.add_widget(continue_wdg)

        home_wdg.add_stretch()
        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg5 = HScrollWidget()
        home_wdg.add_widget(continue_wdg5)

        home_wdg.add_stretch()
        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg4 = HScrollWidget()
        home_wdg.add_widget(continue_wdg4)

        home_wdg.add_stretch()
        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg3 = HScrollWidget()
        home_wdg.add_widget(continue_wdg3)

        home_wdg.add_stretch()
        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg2 = HScrollWidget()
        home_wdg.add_widget(continue_wdg2)

        home_wdg.add_stretch()
        # Continue Watching section title
        continue_watching_title = QLabel("Continue Watching...")
        continue_watching_title.setStyleSheet(cutie_label_style)
        home_wdg.add_widget(continue_watching_title)

        # Horizontal scroll widget with images
        continue_wdg1 = HScrollWidget()
        home_wdg.add_widget(continue_wdg1)

        home_wdg.add_stretch()


        # DEMO IMAGES
        for i in range(20):
            continue_wdg.add_image(resource_path("embedded_images/demo.jpg"))
            continue_wdg1.add_image(resource_path("embedded_images/demo.jpg"))
            continue_wdg2.add_image(resource_path("embedded_images/demo.jpg"))
            continue_wdg3.add_image(resource_path("embedded_images/demo.jpg"))
            continue_wdg4.add_image(resource_path("embedded_images/demo.jpg"))
            continue_wdg5.add_image(resource_path("embedded_images/demo.jpg"))
