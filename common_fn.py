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


#fixme: THIS ENTIRE CLASS BELOW
class SmoothScrollMixin:
    """
    Mixin that adds smooth scroll-wheel animation to ANY widget
    containing a QScrollArea named 'scroll'.

    Requirements:
        - The class using this mixin MUST have:
              self.scroll -> QScrollArea
    """

    def _init_smooth_scroll(self):
        self._scroll_anim = None
        self._scroll_target = 0

    def wheelEvent(self, event):
        if not hasattr(self, "scroll"):
            # Fallback: behave normally
            return super().wheelEvent(event)

        scroll_bar = None
        # Pick horizontal vs vertical automatically
        if self.scroll.horizontalScrollBar().maximum() > 0:
            scroll_bar = self.scroll.horizontalScrollBar()
        elif self.scroll.verticalScrollBar().maximum() > 0:
            scroll_bar = self.scroll.verticalScrollBar()
        else:
            # No scrollable range → do default scroll
            return super().wheelEvent(event)

        # scale wheel input
        delta = event.angleDelta().y() / 4

        # accumulate target
        if self._scroll_anim and self._scroll_anim.state() == QAbstractAnimation.Running:
            self._scroll_target -= delta
        else:
            self._scroll_target = scroll_bar.value() - delta

        # clamp
        self._scroll_target = max(scroll_bar.minimum(),
                                  min(scroll_bar.maximum(), self._scroll_target))

        anim = QPropertyAnimation(scroll_bar, b"value")
        anim.setDuration(150)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.start()
        self._scroll_anim = anim

        event.accept()


class HScrollWidget(QWidget):
    """
    A reusable horizontal scroll widget where you can add widgets (e.g., image covers)
    """
    def __init__(self, parent=None, item_height=200, item_spacing=10, h_scroll_bar=False, v_scroll_bar=False):
        super().__init__(parent)

        # --- settings ---
        self.item_height = item_height
        self.item_spacing = item_spacing

        # --- keep animation state (important!) ---
        self._scroll_anim = None
        self._scroll_target = 0

        # --- main layout ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # --- scroll area ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        if h_scroll_bar:
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        if v_scroll_bar:
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFixedHeight(self.item_height + 20)

        # --- container (holds the horizontal items) ---
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

    def wheelEvent(self, event):
        """
        Smooth horizontal scrolling using an accumulating animation target.
        Guards included so missing attributes or zero-range scroll do not crash.
        """
        try:
            scroll_bar = self.scroll.horizontalScrollBar()
        except Exception:
            event.ignore()
            return

        # If there's no range to scroll, ignore and don't animate
        if scroll_bar.maximum() == scroll_bar.minimum():
            event.ignore()
            return

        # Scale wheel delta for feel; adjust divisor to taste
        delta = event.angleDelta().y()

        # If an animation is running, accumulate into the existing target.
        # Use QAbstractAnimation.Running for the comparison (not the instance attribute).
        if self._scroll_anim and self._scroll_anim.state() == QAbstractAnimation.Running:
            self._scroll_target -= delta
        else:
            self._scroll_target = scroll_bar.value() - delta

        # Clamp target
        self._scroll_target = max(scroll_bar.minimum(), min(scroll_bar.maximum(), self._scroll_target))

        # Create and start an animation from current value -> target
        anim = QPropertyAnimation(scroll_bar, b"value")
        anim.setDuration(500)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.start()

        # Keep reference so GC doesn't kill it mid-animation
        self._scroll_anim = anim

        event.accept()


class VScrollWidget(QWidget):
    """
    A reusable vertical scroll widget where you can add widgets (e.g., image covers)
    """
    def __init__(self, parent=None, item_spacing=10, h_scroll_bar=False, v_scroll_bar=False):
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

        self.scroll.viewport().installEventFilter(self)

        # --- container layout ---
        self.container = QWidget()
        self.v_layout = QVBoxLayout(self.container)
        self.v_layout.setContentsMargins(10, 0, 10, 0)
        self.v_layout.setSpacing(self.item_spacing)

        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)

    def eventFilter(self, obj, event):
        if obj is self.scroll.viewport() and event.type() == event.Type.Wheel:
            return self._handle_wheel(event)
        return super().eventFilter(obj, event)

    def _handle_wheel(self, event):
        scroll_bar = self.scroll.verticalScrollBar()
        if scroll_bar.maximum() == scroll_bar.minimum():
            return False

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
        anim.setDuration(500)
        anim.setStartValue(scroll_bar.value())
        anim.setEndValue(self._scroll_target)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        # Store animation so it doesn't get garbage-collected
        self._scroll_anim = anim

        event.accept()
        return True  # event fully handled

    def add_widget(self, widget):
        self.v_layout.addWidget(widget)

    def add_stretch(self):
        self.v_layout.addStretch()
