from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QApplication

class SvgButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.svg_widget = QSvgWidget(self)
        self.layout.addWidget(self.svg_widget)

    def set_svg(self, filepath):
        self.svg_widget.load(filepath)

    def clear_svg(self):
        self.svg_widget.load('')  # Clear the SVG widget

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())  # Use button's text as mime data
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.MoveAction)
