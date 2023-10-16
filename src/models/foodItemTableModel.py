from PyQt5.QtCore import Qt, QAbstractTableModel


class FoodItemTableModel(QAbstractTableModel):
    def __init__(self):
        super(FoodItemTableModel, self).__init__()
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
        Add food item data to the list to be displayed, duplicate items are not added
        @param foodItems - list of dicts where each dict is a food item to be added
        @return - None
        """

        # get list of ids already in list
        currentIds = []
        for item in self.foodData:
            currentIds.append(item["id"])

        # add new items to list if they are not duplicates
        for item in newFoodItems:
            if item["id"] not in currentIds:
                self.foodData.append(item)

        # update the view
        self.layoutChanged.emit()

    def removeFoodItems(self, indexes: list):
        """
        Remove the food item data at the given indexes
        @param indexes - a list of integers corresponding to indexes in foodData to be removed
        @return - None
        """

        # work backwards so removing does not affect indexes
        indexes = sorted(indexes, reverse=True)

        for i in indexes:
            del self.foodData[i]

        # update the view
        self.layoutChanged.emit()

    # get the selected food item data
    def getSelectedData(self, selectedIndexes: list):
        selectedData = []
        for i in selectedIndexes:
            if "error" in self.foodData[i].keys():
                # do not select errors
                return
            selectedData.append(self.foodData[i])

        return selectedData
