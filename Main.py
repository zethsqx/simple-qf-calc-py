import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import math
import StockReader
import SearchStock

qtCreatorFile = "Main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search)
        
    def search(self):
        SearchStock.scan_file('stocklist.csv',self.stockName.text())
        #print(self.stockName.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
