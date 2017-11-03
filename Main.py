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
        self.searchButton.clicked.connect(self.openStockDialog)
    
    def openStockDialog(self):
        self.dialog = Ui_StockDialog(self, self.stockName.text())
        self.dialog.show()

    def getSharpeList(self):
        pass
        
class Ui_StockDialog(QDialog, ui_SL):
    def __init__(self, parent=None, data=None):
        super(Ui_StockDialog, self).__init__(parent)
        self.setupUi(self)
        if data:
            self.setTableData(data)
            self.show()
        self.okButton.clicked.connect(self.selectStock)
        self.cancelButton.clicked.connect(self.closeDialog)
        
    def setTableData(self, data):
        stocklist = SearchStock.scan_file('stocklist.csv',data)
        index = 0
        for key, value in stocklist.items():
            #print(key, value, index)
            self.stocklistTable.insertRow(index)
            self.stocklistTable.setItem(index, 0, QTableWidgetItem(key.strip("\"")))
            self.stocklistTable.setItem(index, 1, QTableWidgetItem(value.strip("\"")))
            index+=1
        
    def selectStock(self):
        if self.stocklistTable.itemClicked:
            index = self.stocklistTable.selectedIndexes()
            symbol = index[0].data()
            stockname = index[1].data()

            stockList = StockReader.getStock("AAPL")
            sharpeRatio = StockReader.sharpe(stockList)
            #print(sharpeRatio)
            
            main = self.parent()
            row = main.portfolioTable.rowCount()
            main.portfolioTable.insertRow(row)
            main.portfolioTable.setItem(row, 0, QTableWidgetItem(str(row+1)))
            main.portfolioTable.setItem(row, 1, QTableWidgetItem(symbol))
            main.portfolioTable.setItem(row, 2, QTableWidgetItem(stockname))
            main.portfolioTable.setItem(row, 3, QTableWidgetItem(str(sharpeRatio)))
            return self.accept()
        
    def closeDialog(self):
        return self.accept()

def main():
    app = QApplication(sys.argv)
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
