import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QFontDatabase
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

        # add custom font to database
        QFontDatabase.addApplicationFont(
            ":/fonts/resources/fonts/SourceSans3-VariableFont_wght.ttf"
        )

        self.setupUi(self)

        ### set up sidebar button click events ###
        self.sidebarSearchButton.clicked.connect(self.sidebarSearchButtonClicked)
        self.sidebarShoppingButton.clicked.connect(self.sidebarShoppingButtonClicked)
        self.sidebarFridgeButton.clicked.connect(self.sidebarFridgeButtonClicked)
        self.sidebarRecipesButton.clicked.connect(self.sidebarRecipesButtonClicked)
        self.sidebarNutritionButton.clicked.connect(self.sidebarNutritionButtonClicked)

        ### set up open detail page events
        self.searchTableView.doubleClicked.connect(self.openFoodDetailPage)
        self.shoppingTableView.doubleClicked.connect(self.openFoodDetailPage)
        self.fridgeTableView.doubleClicked.connect(self.openFoodDetailPage)

        ### set up search bar events ###
        self.searchLineEdit.returnPressed.connect(self.searchFoodItems)
        self.recipesLineEdit.returnPressed.connect(self.searchRecipes)

        ### set up data movement button events ###
        self.searchAddToShoppingListButton.clicked.connect(self.addToShoppingList)
        self.shoppingRemoveButton.clicked.connect(self.removeFromShoppingList)
        self.fridgeRemoveButton.clicked.connect(self.removeFromFridgeList)
        self.shoppingMoveToFridgeButton.clicked.connect(self.moveToFridgeList)
        self.recipesAddToNutritionListButton.clicked.connect(self.addToNutritionList)

        # set up nutrition spin box update event
        self.nutritionSpinBox.valueChanged.connect(self.updateNutritionLabels)

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

    # get selected nutrition data and open food detail page
    def openFoodDetailPage(self):
        # determine which table to pull data from
        # search page
        selectedData = []
        if self.mainWindowStack.currentIndex() == 0:
            selectedIndexes = (
                self.searchTableView.selectionModel().selectedRows()[0].row()
            )
            selectedData = self.searchTableModel.getSelectedData([selectedIndexes])
        # shopping list page
        elif self.mainWindowStack.currentIndex() == 1:
            selectedIndexes = (
                self.shoppingTableView.selectionModel().selectedRows()[0].row()
            )
            selectedData = self.shoppingTableModel.getSelectedData([selectedIndexes])
        # fridge page
        else:
            selectedIndexes = (
                self.fridgeTableView.selectionModel().selectedRows()[0].row()
            )
            selectedData = self.fridgeTableModel.getSelectedData([selectedIndexes])

        # use search model to get nutrition data for selected food item
        foodItemId = selectedData[0]["id"]

        foodNutritionData = self.searchTableModel.getFoodItemNutrition(foodItemId)

        # set food detail labels before opening page
        # check for error

        self.mainWindowStack.setCurrentIndex(5)

    def setFoodDetailLabels(self, nutritionData):
        pass

    # pass search text to model
    def searchFoodItems(self):
        self.searchTableModel.search(self.searchLineEdit.text())

    # pass search text to model
    def searchRecipes(self):
        searchTerm = self.recipesLineEdit.text()
        ingredients = []

        # add filter to search
        if self.recipesFilterCheckBox.isChecked():
            # get all ingredients in the fridge for filtering
            ingredients = self.fridgeTableModel.getIngredients()

        self.recipesTableModel.search(searchTerm, ingredients)

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

        # add data to nutrition list
        self.nutritionTableModel.addRecipes(selectedData)

        self.updateNutritionLabels()

    def updateNutritionLabels(self):
        """
        Calls the nutrition aggregation algorithm to update the labels
        """
        recipes = self.nutritionTableModel.recipeData
        numOfDays = self.nutritionSpinBox.value()

        # run nutrition algorithm
        nutritionData = self.nutritionTableModel.getAggregateRecipeNutrition(numOfDays)
        recommendedData = self.nutritionTableModel.getAggregateRecommendedNutrition(
            numOfDays
        )

        # set data to labels
        self.nutritionCaloriesInfoLabel.setText(
            format(int(nutritionData["calories"]), ",")
            + "/"
            + format(int(recommendedData["calories"]), ",")
            + " kCal"
        )
        self.nutritionTotalFatInfoLabel.setText(
            format(int(nutritionData["fat"]), ",")
            + "/"
            + format(int(recommendedData["fat"]), ",")
            + " g"
        )
        self.nutritionSaturatedFatInfoLabel.setText(
            format(int(nutritionData["saturatedfat"]), ",")
            + "/"
            + format(int(recommendedData["saturatedfat"]), ",")
            + " g"
        )
        self.nutritionCholesterolInfoLabel.setText(
            format(int(nutritionData["cholesterol"]), ",")
            + "/"
            + format(int(recommendedData["cholesterol"]), ",")
            + " mg"
        )
        self.nutritionSodiumInfoLabel.setText(
            format(int(nutritionData["sodium"]), ",")
            + "/"
            + format(int(recommendedData["sodium"]), ",")
            + " mg"
        )
        self.nutritionTotalCarbsInfoLabel.setText(
            format(int(nutritionData["carbohydrates"]), ",")
            + "/"
            + format(int(recommendedData["carbohydrates"]), ",")
            + " g"
        )
        self.nutritionFibersInfoLabel.setText(
            format(int(nutritionData["fiber"]), ",")
            + "/"
            + format(int(recommendedData["fiber"]), ",")
            + " g"
        )
        self.nutritionAddedSugarsInfoLabel.setText(
            format(int(nutritionData["sugar"]), ",")
            + "/"
            + format(int(recommendedData["sugar"]), ",")
            + " g"
        )
        self.nutritionProteinInfoLabel.setText(
            format(int(nutritionData["protein"]), ",")
            + "/"
            + format(int(recommendedData["protein"]), ",")
            + " g"
        )


# create app and window instance
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
