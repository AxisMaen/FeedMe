from PyQt5.QtCore import Qt, QAbstractTableModel
from controllers.recipeController import RecipeController


class RecipeTableModel(QAbstractTableModel):
    def __init__(self):
        super(RecipeTableModel, self).__init__()
        self.recipeData = []
        self.controller = RecipeController()

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
