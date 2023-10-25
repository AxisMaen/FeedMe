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
    def search(self, searchTerm):
        self.recipeData = self.controller.getRecipeData(searchTerm)

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
