import sys
from PyQt5 import QtWidgets
from pages.MainWindow_ui import Ui_FeedMe


class MainWindow(QtWidgets.QMainWindow, Ui_FeedMe):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        ### set up sidebar button click events ###
        self.sidebarSearchButton.clicked.connect(self.sidebarSearchButtonClicked)
        self.sidebarShoppingButton.clicked.connect(self.sidebarShoppingButtonClicked)
        self.sidebarFridgeButton.clicked.connect(self.sidebarFridgeButtonClicked)
        self.sidebarRecipesButton.clicked.connect(self.sidebarRecipesButtonClicked)

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


# create app and window instance
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
