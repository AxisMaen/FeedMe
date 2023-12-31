from PyQt5.QtCore import Qt, QAbstractTableModel
from controllers.recipesController import RecipesController


class RecipesTableModel(QAbstractTableModel):
    def __init__(self):
        super(RecipesTableModel, self).__init__()
        self.recipeData = []
        self.controller = RecipesController()

    def data(self, index, role):
        recipeItem = self.recipeData[index.row()]

        if index.column() == 1:
            if role == Qt.DisplayRole:
                if "error" in recipeItem.keys():
                    return recipeItem["error"]
                return recipeItem["name"]

    def rowCount(self, index):
        return len(self.recipeData)

    def columnCount(self, index):
        return 2

    # get new data and emit signal to update view
    def search(self, searchTerm: str, ingredients: list):
        self.recipeData = self.controller.getRecipeData(searchTerm, ingredients)

        # update the view
        self.layoutChanged.emit()

    # get the selected recipe data
    def getSelectedData(self, selectedIndexes: list):
        selectedData = []
        for i in selectedIndexes:
            if "error" in self.recipeData[i].keys():
                # do not select errors
                return
            selectedData.append(self.recipeData[i])

        return selectedData

    def getRecipeIngredients(self, recipeId: int) -> list:
        """
        Get all the ingredients in the recipe with the given id
        @return - list of strings where each string describes the ingredient and its quantity
        """

        return self.controller.getRecipeIngredients(recipeId)

    def getRecipeInstructions(self, recipeId: int) -> list:
        """
        Get all the instructions in the recipe with the given id
        @return - list of strings where each string describes an instruction, list is ordered by the order of the instructions
        """

        return self.controller.getRecipeInstructions(recipeId)
