from PyQt5.QtCore import Qt, QAbstractTableModel


class ShoppingTableModel(QAbstractTableModel):
    def __init__(self):
        super(ShoppingTableModel, self).__init__()
        self.foodData = []

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

    def addFoodItems(self, newFoodItems: list):
        """
        Add food item data to the shopping list to be displayed, duplicate items are not added
        @param foodItems - list of dicts where each dict is a food item to be added
        @return - None
        """

        # get list of ids already in shopping list
        currentIds = []
        for item in self.foodData:
            currentIds.append(item["id"])

        # add new items to shopping list if they are not duplicates
        for item in newFoodItems:
            if item["id"] not in currentIds:
                self.foodData.append(item)

        # update the view
        self.layoutChanged.emit()
