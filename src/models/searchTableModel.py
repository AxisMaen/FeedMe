from PyQt5.QtCore import Qt, QAbstractTableModel
from controllers.foodItemController import FoodItemController


class SearchTableModel(QAbstractTableModel):
    def __init__(self):
        super(SearchTableModel, self).__init__()
        self.foodData = []
        self.controller = FoodItemController()

    def data(self, index, role):
        foodItem = self.foodData[index.row()]

        if index.column() == 1:
            if role == Qt.DisplayRole:
                if "error" in foodItem.keys():
                    return foodItem["error"]
                return foodItem["name"]

    def rowCount(self, index):
        return len(self.foodData)

    def columnCount(self, index):
        return 2

    # get new data and emit signal to update view
    def search(self, searchTerm):
        self.foodData = self.controller.getFoodData(searchTerm)

        # update the view
        self.layoutChanged.emit()

    # get the selected food item data
    def getSelectedData(self, selectedIndexes: list):
        selectedData = []
        for i in selectedIndexes:
            if "error" in self.foodData[i].keys():
                # do not add errors to shopping list
                return
            selectedData.append(self.foodData[i])

        return selectedData
