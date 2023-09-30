from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QLabel
from controllers.foodItemController import FoodItemController


class SearchTableModel(QAbstractTableModel):
    def __init__(self):
        super(SearchTableModel, self).__init__()
        self.foodData = []
        self.controller = FoodItemController()

    def data(self, index, role):
        foodItem = self.foodData[index.row()]

        if index.column() == 0:
            if role == Qt.DecorationRole:
                label = QLabel()
                pixmap = foodItem[index.column()]
                label.setPixmap(pixmap)
                return label
        if index.column() == 1:
            if role == Qt.DisplayRole:
                return foodItem[index.column()]

    def rowCount(self, index):
        return len(self.foodData)

    def columnCount(self, index):
        return 2

    # get new data and emit signal to update view
    def search(self, searchTerm):
        self.foodData = self.controller.getFoodData(searchTerm)

        # update the view
        self.layoutChanged.emit()
