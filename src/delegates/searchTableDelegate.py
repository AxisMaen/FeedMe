from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QColor, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize


class SearchTableDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.fillRect(option.rect, QColor(191, 222, 185))

        model = index.model()
        try:
            pixmap = model.foodData[index.row()]["pixmap"]

            pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio)
            painter.drawPixmap(option.rect, pixmap)
        except:
            # if the pixmap cannot be drawn, draw blank pixmap
            pixmap = QPixmap(100, 100)
            pixmap.fill(Qt.white)
            painter.drawPixmap(option.rect, pixmap)

    def sizeHint(self, option, index):
        return QSize(100, 100)
