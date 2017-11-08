import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import math
import StockReader
import StockAllocation
import SearchStock
import multiprocessing
from CustomExceptions import *

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
ui_MW, QtBaseClass = uic.loadUiType("Main.ui")
ui_SL, QtBaseClass = uic.loadUiType("StockList.ui")
ui_IV, QtBaseClass = uic.loadUiType("Investment.ui")

#Main Window 
class Ui_MainWindow(QMainWindow, ui_MW):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.openStockDialog)
        self.deleteButton.clicked.connect(self.deleteStock)
        self.investButton.clicked.connect(self.openInvestmentDialog)
    
    def openStockDialog(self):
        self.dialog = Ui_StockDialog(self, self.stockName.text())
        self.dialog.show()

    def openInvestmentDialog(self):
        self.dialog = Ui_InvestmentDialog(self)
        self.dialog.show()

    def deleteStock(self):
        if self.portfolioTable.itemClicked:
            self.portfolioTable.removeRow(self.portfolioTable.currentRow())
            for i in range(0, self.portfolioTable.rowCount()):
                self.portfolioTable.setItem(i, 0, QTableWidgetItem(str(i+1)))
                self.portfolioTable.setItem(i, 1, QTableWidgetItem(self.portfolioTable.item(i,1)))
                self.portfolioTable.setItem(i, 2, QTableWidgetItem(self.portfolioTable.item(i,2)))
                self.portfolioTable.setItem(i, 3, QTableWidgetItem(self.portfolioTable.item(i,3)))

    def getSharpeDict(self):
        sharpelist = {}
        for i in range(0, self.portfolioTable.rowCount()):
            sharpelist.update({self.portfolioTable.item(i,1).text():float(self.portfolioTable.item(i,3).text())})
        print("Gotten your SHARPEDICT")
        print(sharpelist)
        return sharpelist

# Dialog for selecting the stock
class Ui_StockDialog(QDialog, ui_SL):
    def __init__(self, parent=None, data=None):
        super(Ui_StockDialog, self).__init__(parent)
        self.setupUi(self)
        self.setTableData(data)
        self.show()
        
        self.okButton.clicked.connect(self.okBtn)
        self.cancelButton.clicked.connect(self.closeDialog)
        
    def setTableData(self, data):
        stocklist = SearchStock.scan_file('stocklist.csv',data)
        if len(stocklist) == 0:
            raise StockNotFoundException('Stock symbol not found','')
        index = 0
        for key, value in stocklist.items():
            #print(key, value, index)
            self.stocklistTable.insertRow(index)
            self.stocklistTable.setItem(index, 0, QTableWidgetItem(key.strip("\"")))
            self.stocklistTable.setItem(index, 1, QTableWidgetItem(value.strip("\"")))
            index+=1
            
    def okBtn(self):
        if self.stocklistTable.itemClicked:
            index = self.stocklistTable.selectedIndexes()
            symbol = index[0].data()
            stockname = index[1].data()
            
            stockList = StockReader.getStock(symbol)
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

#Dialog for inputting investment amount and stock amt
class Ui_InvestmentDialog(QDialog, ui_IV):
    global CURRDIAL
    CURRDIAL = 0
    def __init__(self, parent=None):
        super(Ui_InvestmentDialog, self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.stockDial.sliderMoved.connect(self.changeValue)
        self.okButton.clicked.connect(self.okBtn)
        self.cancelButton.clicked.connect(self.closeDialog)

    def okBtn(self):
        main = self.parent()
        main.stockLCD.display(self.stockAmt.text())
        main.investLabel.setText(self.investAmt.text())

        resultDict = StockAllocation.getInvestDecision(main.getSharpeDict(), int(self.stockAmt.text()), float(self.investAmt.text()))

        main.investTable.clear()
        main.investTable.setRowCount(0)
        i = 0
        for k,v in resultDict.items():
            main.investTable.insertRow(i)
            main.investTable.setItem(i, 0, QTableWidgetItem(str(k)))
            main.investTable.setItem(i, 1, QTableWidgetItem(str(v)))
            i += 1
            
        return self.accept()
    
    def changeValue(self):
        global CURRDIAL
        if self.stockDial.value() > CURRDIAL:
            self.stockAmt.setText(str(int(self.stockAmt.text())+1))
        else:
            val = int(self.stockAmt.text()) - 1
            self.stockAmt.setText(str(val))
            if val <= 0:
                self.stockAmt.setText(str(0))
        CURRDIAL = self.stockDial.value()

    def closeDialog(self):
        return self.accept()

def main():
    app = QApplication(sys.argv)
    main = Ui_MainWindow()
    main.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
