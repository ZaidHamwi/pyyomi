import os
import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QAbstractAnimation, QEasingCurve
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLabel


def write_to_appdata(relative_path, data):
    # Get the path to the Roaming AppData directory
    appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

    # Create the full path for the specified subdirectory and file
    full_path = os.path.join(appdata_path, relative_path)

    # Check if the file exists
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        print('Missing files and directories will be restored')

    # Extract the directory part of the full path
    directory = os.path.dirname(full_path)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Write to the file
    with open(full_path, 'w') as f:
        f.write(data)

    print(f"Data written to: {full_path}")

def read_from_appdata(relative_path):
    # Get the path to the Roaming AppData directory
    appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

    # Create the full path for the specified subdirectory and file
    full_path = os.path.join(appdata_path, relative_path)

    # Check if the file exists
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        print('Missing files and directories will be restored')
        return None

    # Read the file
    with open(full_path, 'r') as f:
        data = f.read()

    print(f"Data read from: {full_path}")
    return data

def resource_path(relative_path):
    """ Get the absolute path to the resource (for both exe and dev modes) """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in development mode, get the folder of the main script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

# Stylesheets
title_label_style = """
QLabel {
    color: white;
    background-color: #444444;
    font-size: 20px;
    font-weight: bold;
    padding: 4px;
    border-radius: 8px;
}
"""
bold_label_style = """
QLabel {
    color: white;
    font-size: 15px;
    font-weight: bold;
}
"""

# Lines
class VLine(QWidget):
    def __init__(self):
        super().__init__(None)


class HScrollWidget(QWidget):
    """
    A reusable horizontally scrollable widget with smooth scrolling.
    Perfect for image covers, playlists, rows of cards, etc.
    """
    def __init__(self, parent=None, item_height=200, item_spacing=10,
                 h_scroll_bar=False, v_scroll_bar=False):
        super().__init__(parent)

        self.item_height = item_height
        self.item_spacing = item_spacing

        self._scroll_anim = None
        self._scroll_target = 0

        # --- main layout ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # --- scroll area ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(self.item_height + 20)

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if h_scroll_bar else Qt.ScrollBarAlwaysOff
        )
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if v_scroll_bar else Qt.ScrollBarAlwaysOff
        )

        # IMPORTANT: catch wheel events on the viewport
        self.scroll.viewport().installEventFilter(self)

        # --- container that holds row items ---
        self.container = QWidget()
        self.h_layout = QHBoxLayout(self.container)
        self.h_layout.setContentsMargins(10, 0, 10, 0)
        self.h_layout.setSpacing(self.item_spacing)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

    # -------------------------------------------------------------
    # Event filter to capture wheel events (ALWAYS works)
    # -------------------------------------------------------------
    def eventFilter(self, obj, event):
        if obj is self.scroll.viewport() and event.type() == event.Type.Wheel:
            return self._handle_wheel(event)
        return super().eventFilter(obj, event)

    # -------------------------------------------------------------
    # Smooth horizontal wheel scrolling
    # -------------------------------------------------------------
    def _handle_wheel(self, event):
        scroll_bar = self.scroll.horizontalScrollBar()

        # If no scrolling possible
        if scroll_bar.maximum() == scroll_bar.minimum():
            return False

        # Horizontal scrolling uses vertical wheel delta (.y)
        delta = event.angleDelta().y()

        # Accumulate if animation running
        if self._scroll_anim and self._scroll_anim.state() == QAbstractAnimation.Running:
            self._scroll_target -= delta
        else:
            self._scroll_target = scroll_bar.value() - delta

        # Clamp
        self._scroll_target = max(scroll_bar.minimum(),
                                  min(scroll_bar.maximum(), self._scroll_target))

        # Animate
        anim = QPropertyAnimation(scroll_bar, b"value")
        anim.setDuration(400)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        self._scroll_anim = anim

        event.accept()
        return True

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------
    def add_widget(self, widget: QWidget):
        widget.setFixedHeight(self.item_height)
        self.h_layout.addWidget(widget)

    def add_image(self, image_path: str):
        label = QLabel()
        pix = QPixmap(image_path)

        if pix.isNull():
            print(f"Warning: could not load image '{image_path}'")
            return

        pix = pix.scaledToHeight(self.item_height, Qt.SmoothTransformation)
        label.setPixmap(pix)
        label.setFixedSize(pix.size())
        label.setScaledContents(True)
        label.setCursor(Qt.PointingHandCursor)

        self.add_widget(label)


class VScrollWidget(QWidget):
    """
    A reusable horizontally scrollable widget with smooth scrolling.
    Perfect for app pages, like a settings page.
    """
    def __init__(self, parent=None, item_spacing=10, h_scroll_bar=False, v_scroll_bar=True):
        super().__init__(parent)

        self.item_spacing = item_spacing
        self._scroll_target = 0
        self._scroll_anim = None

        # --- main layout ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # --- scroll area ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if h_scroll_bar else Qt.ScrollBarAlwaysOff
        )
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if v_scroll_bar else Qt.ScrollBarAlwaysOff
        )

        # IMPORTANT: Install wheel filter so we ALWAYS catch scroll events
        self.scroll.viewport().installEventFilter(self)

        # --- container layout ---
        self.container = QWidget()
        self.v_layout = QVBoxLayout(self.container)
        self.v_layout.setContentsMargins(10, 0, 10, 0)
        self.v_layout.setSpacing(self.item_spacing)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

    # -------------------------------------------------------------
    # ALWAYS receive wheel events via eventFilter
    # -------------------------------------------------------------
    def eventFilter(self, obj, event):
        if obj is self.scroll.viewport() and event.type() == event.Type.Wheel:
            return self._handle_wheel(event)
        return super().eventFilter(obj, event)

    # -------------------------------------------------------------
    # Smooth scrolling
    # -------------------------------------------------------------
    def _handle_wheel(self, event):
        scroll_bar = self.scroll.verticalScrollBar()

        # If no scrolling needed
        if scroll_bar.maximum() == scroll_bar.minimum():
            return False

        # Stronger delta (smooth but noticeable)
        delta = event.angleDelta().y()

        # If an animation is running, accumulate
        if self._scroll_anim and self._scroll_anim.state() == QAbstractAnimation.Running:
            self._scroll_target -= delta
        else:
            self._scroll_target = scroll_bar.value() - delta

        # Clamp
        self._scroll_target = max(scroll_bar.minimum(),
                                  min(scroll_bar.maximum(), self._scroll_target))

        # Animation
        anim = QPropertyAnimation(scroll_bar, b"value")
        anim.setDuration(400)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        # Store animation so it doesn't get garbage-collected
        self._scroll_anim = anim

        event.accept()
        return True  # event fully handled

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------
    def add_widget(self, widget):
        self.v_layout.addWidget(widget)

    def add_stretch(self):
        self.v_layout.addStretch()
