import sys
from PyQt5.QtWidgets import QMainWindow, QTableView, QApplication
from PyQt5 import uic

assetAllocaterView = "AssetAllocaterView.ui"
UI_mainwindow, QtBaseClass = uic.loadUiType(assetAllocaterView)
print(UI_mainwindow, type(QtBaseClass))

class Main(QMainWindow, UI_mainwindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
