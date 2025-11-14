import os
import sys


from PySide6.QtCore import Qt, QPropertyAnimation, QAbstractAnimation
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


# For reading embedded files
# def resource_path(relative_path):
#     """ Get the absolute path to the resource (for both exe and dev modes) """
#     try:
#         # If the application is running as a PyInstaller executable
#         base_path = sys._MEIPASS
#     except AttributeError:
#         # If running in development mode
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)

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
cutie_label_style = """
QLabel {
    color: white;
    background-color: #444444;
    font-size: 15px;
    font-weight: bold;
    padding: 4px;
    border-radius: 8px;
}
"""
boldie_label_style = """
QLabel {
    color: white;
    font-size: 14px;
    font-weight: bold;
}
"""


class ScrollWidget(QWidget):
    """
    A reusable horizontal scroll widget where you can add widgets (e.g., image covers)
    """
    def __init__(self, parent=None, item_height=200, item_spacing=10):
        super().__init__(parent)

        self.item_height = item_height
        self.item_spacing = item_spacing

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFixedHeight(self.item_height + 20)  # space for scrollbar

        # Container inside scroll
        self.container = QWidget()
        self.h_layout = QHBoxLayout(self.container)
        self.h_layout.setContentsMargins(10, 0, 10, 0)
        self.h_layout.setSpacing(self.item_spacing)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

    def add_widget(self, widget: QWidget):
        """
        Add a widget to the scroll area.
        Forces the widget to have the fixed height of this scroll widget.
        """
        widget.setFixedHeight(self.item_height)
        self.h_layout.addWidget(widget)

    def add_image(self, image_path: str):
        """
        Add an image QLabel, automatically scaled to fixed height while preserving aspect ratio.
        """
        label = QLabel()
        pix = QPixmap(image_path)
        if pix.isNull():
            print(f"Warning: could not load image '{image_path}'")
            return

        # Scale to fixed height, keep aspect ratio
        pix = pix.scaledToHeight(self.item_height, Qt.SmoothTransformation)
        label.setPixmap(pix)
        label.setFixedSize(pix.size())
        label.setScaledContents(True)
        label.setCursor(Qt.PointingHandCursor)
        self.add_widget(label)

        self._scroll_anim = None
        self._scroll_target = 0

    def wheelEvent(self, event):
        scroll_bar = self.scroll.horizontalScrollBar()
        delta = event.angleDelta().y() / 2  # scale for smooth feel

        # Update the target position
        if self._scroll_anim and self._scroll_anim.state() == QAbstractAnimation.Running:
            # If animation is running, accumulate movement
            self._scroll_target -= delta
        else:
            # Start from current value
            self._scroll_target = scroll_bar.value() - delta

        # Clamp to scroll range
        self._scroll_target = max(scroll_bar.minimum(), min(scroll_bar.maximum(), self._scroll_target))

        # Create animation
        anim = QPropertyAnimation(scroll_bar, b"value")
        anim.setDuration(150)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.start()

        # Prevent garbage collection
        self._scroll_anim = anim

        event.accept()
