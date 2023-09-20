from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from controllers.foodItemController import FoodItemController

"""
class SearchListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, foodItems=[], **kwargs):
        super(SearchListModel, self).__init__(*args, **kwargs)
        self.foodItems = foodItems

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            status, text = self.foodItems[index.row()]
            return text

    def rowCount(self, index):
        return len(self.foodItems)
"""


class SearchListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(SearchListModel, self).__init__()
        self.foodItems = []
        self.controller = FoodItemController()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # testing by just displaying food item names
            itemName = self.foodItems[index.row()]
            return itemName

    def rowCount(self, index):
        return len(self.foodItems)

    # get new data and emit signal to update view
    def search(self, searchTerm):
        self.foodItems = self.controller.getFoodItems(searchTerm)
        self.layoutChanged.emit()
