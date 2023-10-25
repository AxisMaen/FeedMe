import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from pages.MainWindow_ui import Ui_FeedMe
from models.searchTableModel import SearchTableModel
from models.foodItemTableModel import FoodItemTableModel
from models.recipesTableModel import RecipesTableModel
from models.nutritionTableModel import NutritionTableModel
from delegates.foodItemTableDelegate import FoodItemTableDelegate
from delegates.recipesTableDelegate import RecipesTableDelegate


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
        self.shoppingRemoveButton.clicked.connect(self.removeFromShoppingList)
        self.fridgeRemoveButton.clicked.connect(self.removeFromFridgeList)
        self.shoppingMoveToFridgeButton.clicked.connect(self.moveToFridgeList)
        self.recipesAddToNutritionListButton.clicked.connect(self.addToNutritionList)

        ### link views to models ###
        # food search page
        self.searchTableModel = SearchTableModel()
        self.searchTableView.setModel(self.searchTableModel)

        # shopping list page
        self.shoppingTableModel = FoodItemTableModel()
        self.shoppingTableView.setModel(self.shoppingTableModel)

        # fridge list page
        self.fridgeTableModel = FoodItemTableModel()
        self.fridgeTableView.setModel(self.fridgeTableModel)

        # recipes page
        self.recipesTableModel = RecipesTableModel()
        self.recipesTableView.setModel(self.recipesTableModel)

        # nutrition page
        self.nutritionTableModel = NutritionTableModel()
        self.nutritionTableView.setModel(self.nutritionTableModel)

        ### set image height for views ###
        self.searchTableView.verticalHeader().setDefaultSectionSize(100)
        self.shoppingTableView.verticalHeader().setDefaultSectionSize(100)
        self.fridgeTableView.verticalHeader().setDefaultSectionSize(100)
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

        # fridge page
        self.fridgeTableImageDelegate = FoodItemTableDelegate(self.fridgeTableView)
        self.fridgeTableView.setItemDelegateForColumn(0, self.fridgeTableImageDelegate)

        # recipes page
        self.recipesTableImageDelegate = RecipesTableDelegate(self.recipesTableView)
        self.recipesTableView.setItemDelegateForColumn(
            0, self.recipesTableImageDelegate
        )

        ### set view fonts ###
        self.searchTableView.setFont(QFont("Source Sans 3", 12))
        self.shoppingTableView.setFont(QFont("Source Sans 3", 12))
        self.fridgeTableView.setFont(QFont("Source Sans 3", 12))
        self.recipesTableView.setFont(QFont("Source Sans 3", 12))
        self.nutritionTableView.setFont(QFont("Source Sans 3", 12))

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
        self.recipesTableModel.search(self.recipesLineEdit.text())

    # get selected food item data and pass to shopping list model
    def addToShoppingList(self):
        selectedModelIndexes = self.searchTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        selectedData = self.searchTableModel.getSelectedData(selectedIndexes)

        self.shoppingTableModel.addFoodItems(selectedData)

    # get selected indexes and remove the cooresponding food item data
    def removeFromShoppingList(self):
        selectedModelIndexes = self.shoppingTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        self.shoppingTableModel.removeFoodItems(selectedIndexes)

    # get selected indexes and remove the cooresponding food item data
    def removeFromFridgeList(self):
        selectedModelIndexes = self.fridgeTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        self.fridgeTableModel.removeFoodItems(selectedIndexes)

    def moveToFridgeList(self):
        selectedModelIndexes = self.shoppingTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        selectedData = self.shoppingTableModel.getSelectedData(selectedIndexes)

        # add data to fridge list
        self.fridgeTableModel.addFoodItems(selectedData)

        # remove data from shopping list
        self.removeFromShoppingList()

    def addToNutritionList(self):
        selectedModelIndexes = self.recipesTableView.selectionModel().selectedRows()

        # convert QModelIndex(s) to integer indexes
        selectedIndexes = []
        for i in selectedModelIndexes:
            selectedIndexes.append(i.row())

        selectedData = self.recipesTableModel.getSelectedData(selectedIndexes)

        # add data to fridge list
        self.nutritionTableModel.addRecipes(selectedData)


# create app and window instance
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
