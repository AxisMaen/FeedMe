from PyQt5.QtCore import Qt, QAbstractTableModel

# from controllers.nutritionController import NutritionController


class NutritionTableModel(QAbstractTableModel):
    def __init__(self):
        super(NutritionTableModel, self).__init__()
        self.recipeData = []

    def data(self, index, role):
        recipeItem = self.recipeData[index.row()]

        if index.column() == 0:
            if role == Qt.DisplayRole:
                if "error" in recipeItem.keys():
                    return recipeItem["error"]
                return recipeItem["name"]

    def rowCount(self, index):
        return len(self.recipeData)

    def columnCount(self, index):
        return 1

    def addRecipes(self, recipes):
        """
        Add recipe data to the list to be displayed, duplicate items are added
        @param recipes - list of dicts where each dict is a recipe to be added (nutrition information not included)
        @return - None
        """

        # add new recipes to model
        for recipe in recipes:
            self.recipeData.append(recipe)

        # update the view
        self.layoutChanged.emit()
