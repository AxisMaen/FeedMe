import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from pages.MainWindow_ui import Ui_FeedMe
from models.searchTableModel import SearchTableModel
from delegates.searchTableDelegate import SearchTableDelegate


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
        self.searchLineEdit.returnPressed.connect(self.searchFoodItem)

        ### link views to models ###
        self.searchListModel = SearchTableModel()
        self.searchTableView.setModel(self.searchListModel)

        ### set image height for views ###
        self.searchTableView.verticalHeader().setDefaultSectionSize(100)

        ### set view delegates ###
        self.searchTableImageDelegate = SearchTableDelegate(self.searchTableView)
        self.searchTableView.setItemDelegateForColumn(0, self.searchTableImageDelegate)

        ### set view fonts ###
        self.searchTableView.setFont(QFont("Source Sans 3", 12))

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
    def searchFoodItem(self):
        self.searchListModel.search(self.searchLineEdit.text())


# create app and window instance
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
