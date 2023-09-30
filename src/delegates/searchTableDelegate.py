from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QColor, QImage, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize


class SearchTableDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.fillRect(option.rect, QColor(191, 222, 185))

        model = index.model()

        pixmap = model.foodData[index.row()][0]

        pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio)
        painter.drawPixmap(option.rect, pixmap)

    def sizeHint(self, option, index):
        return QSize(100, 100)
