import sys
from PyQt5 import QtWidgets
from pages.MainWindow_ui import Ui_FeedMe


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_FeedMe()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
