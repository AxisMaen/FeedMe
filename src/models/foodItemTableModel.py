from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QPixmap
import os
import sys
import pickle
from qtHelpers.Pickled_QPixmap import Pickled_QPixmap


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

    def getIngredients(self):
        """
        Get the names of all ingredients in the model
        @return - list of strings where each item is the name of an ingredient
        """
        names = []
        for item in self.foodData:
            names.append(item["name"])

        return names

    def saveData(self, filename: str):
        """
        Load data in the model to a pickle file. This will overwrite any existing data
        @param filename - name of the file to save data to (extension included)
        """

        try:
            path = os.path.join(
                os.path.dirname(os.path.abspath(sys.argv[0])),
                "FeedMeData",
                filename,
            )

            # create the path to save data if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)

            # QPixmaps cannot be pickled, use substitute class
            saveData = self.foodData
            for foodItem in saveData:
                # replace pixmaps with substitutes
                foodItem["pixmap"] = Pickled_QPixmap(foodItem["pixmap"])

            with open(path, "wb") as file:
                pickle.dump(saveData, file)
        except:
            return

    def loadData(self, filename):
        """
        Load data from a pickle file into the model
        If the pickle file is not found or is invalid, import nothing
        @param filename - name of the file to save data to (extension included)
        """
        try:
            path = os.path.join(
                os.path.dirname(os.path.abspath(sys.argv[0])),
                "FeedMeData",
                filename,
            )

            with open(path, "rb") as file:
                loadedData = pickle.load(file)

                # convert Pickled_QPixmap to normal QPixamp
                for foodItem in loadedData:
                    # replace pixmaps with substitutes
                    foodItem["pixmap"] = QPixmap(foodItem["pixmap"])

                self.foodData = loadedData

            # update the view
            self.layoutChanged.emit()
        except:
            # do not load data if there is an error
            return
