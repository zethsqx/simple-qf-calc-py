import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import math
import StockReader
import SearchStock

ui_MW, QtBaseClass = uic.loadUiType("Main.ui")
ui_SL, QtBaseClass = uic.loadUiType("StockList.ui")

class Ui_MainWindow(QMainWindow, ui_MW):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search)
        print("asdaad")
        
    def search(self):
        self.dialog = Ui_StockDialog(self, self.stockName.text())
        self.dialog.show()
        
class Ui_StockDialog(QDialog, ui_SL):
    def __init__(self, parent, data):
        super(Ui_StockDialog, self).__init__(parent)
        self.setupUi(self)
        self.setTableData(data)
        self.okButton.clicked.connect(self.selectStock)
        
    def setTableData(self, data):
        stocklist = SearchStock.scan_file('stocklist.csv',data)
        index = 0
        for key, value in stocklist.items():
            print(key, value, index)
            self.stocklistTable.insertRow(index)
            self.stocklistTable.setItem(index, 0, QTableWidgetItem(key))
            self.stocklistTable.setItem(index, 1, QTableWidgetItem(value))
            index+=1
        
    def selectStock(self):
        if self.stocklistTable.itemClicked:
            index = self.stocklistTable.selectedIndexes()
            self.result = index[0].data()
            return self.accept()

def main():
    app = QApplication(sys.argv)
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
