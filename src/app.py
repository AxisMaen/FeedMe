import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from pages.MainWindow_ui import Ui_FeedMe
from models.searchTableModel import SearchTableModel
from models.shoppingTableModel import ShoppingTableModel
from models.recipeTableModel import RecipeTableModel
from delegates.foodItemTableDelegate import FoodItemTableDelegate
from delegates.recipeTableDelegate import RecipeTableDelegate


class MainWindow(QtWidgets.QMainWindow, Ui_FeedMe):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        ### set up sidebar button click events ###
        self.sidebarSearchButton.clicked.connect(self.sidebarSearchButtonClicked)
        self.sidebarShoppingButton.clicked.connect(self.sidebarShoppingButtonClicked)
        self.sidebarFridgeButton.clicked.connect(self.sidebarFridgeButtonClicked)
        self.sidebarRecipesButton.clicked.connect(self.sidebarRecipesButtonClicked)
        self.sidebarNutritionButton.clicked.connect(self.sidebarNutritionButtonClicked)

        ### set up search bar events ###
        self.searchLineEdit.returnPressed.connect(self.searchFoodItems)
        self.recipesLineEdit.returnPressed.connect(self.searchRecipes)

        ### set up data movement button events ###
        self.searchAddToShoppingListButton.clicked.connect(self.addToShoppingList)

        ### link views to models ###
        # food search page
        self.searchTableModel = SearchTableModel()
        self.searchTableView.setModel(self.searchTableModel)

        # shopping list page
        self.shoppingTableModel = ShoppingTableModel()
        self.shoppingTableView.setModel(self.shoppingTableModel)

        # recipe page
        self.recipeTableModel = RecipeTableModel()
        self.recipesTableView.setModel(self.recipeTableModel)

        ### set image height for views ###
        self.searchTableView.verticalHeader().setDefaultSectionSize(100)
        self.shoppingTableView.verticalHeader().setDefaultSectionSize(100)
        self.recipesTableView.verticalHeader().setDefaultSectionSize(100)

        ### set view delegates ###
        # food search page
        self.searchTableImageDelegate = FoodItemTableDelegate(self.searchTableView)
        self.searchTableView.setItemDelegateForColumn(0, self.searchTableImageDelegate)

        # shopping list page
        self.shoppingTableImageDelegate = FoodItemTableDelegate(self.shoppingTableView)
        self.shoppingTableView.setItemDelegateForColumn(
            0, self.shoppingTableImageDelegate
        )

        # recipe page
        self.recipeTableImageDelegate = RecipeTableDelegate(self.recipesTableView)
        self.recipesTableView.setItemDelegateForColumn(0, self.recipeTableImageDelegate)

        ### set view fonts ###
        self.searchTableView.setFont(QFont("Source Sans 3", 12))
        self.shoppingTableView.setFont(QFont("Source Sans 3", 12))
        self.recipesTableView.setFont(QFont("Source Sans 3", 12))

    # switch to search food page when sidebar button is clicked
    def sidebarSearchButtonClicked(self):
        self.mainWindowStack.setCurrentIndex(0)

    # switch to shopping list page when sidebar button is clicked
    def sidebarShoppingButtonClicked(self):
        self.mainWindowStack.setCurrentIndex(1)

    # switch to my fridge page when sidebar button is clicked
    def sidebarFridgeButtonClicked(self):
        self.mainWindowStack.setCurrentIndex(2)

    # switch to recipes page when sidebar button is clicked
    def sidebarRecipesButtonClicked(self):
        self.mainWindowStack.setCurrentIndex(3)

    # switch to recipes page when sidebar button is clicked
    def sidebarNutritionButtonClicked(self):
        self.mainWindowStack.setCurrentIndex(4)

    # pass search text to model
    def searchFoodItems(self):
        self.searchTableModel.search(self.searchLineEdit.text())

    # pass search text to model
    def searchRecipes(self):
        self.recipeTableModel.search(self.recipesLineEdit.text())

    # get selected food item data and pass to shopping list model
    def addToShoppingList(self):
        selectedModelIndexes = self.searchTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        selectedData = self.searchTableModel.getSelectedData(selectedIndexes)

        self.shoppingTableModel.addFoodItems(selectedData)


# create app and window instance
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
