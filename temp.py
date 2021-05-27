import sys 
from PyQt5 import QtCore, QtWidgets, uic 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate, Qt

form_class =uic.loadUiType("app.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('날씨 출력 프로그램')
        self.setWindowIcon(QIcon('weather.png'))
        self.date = QDate.currentDate()
        self.initUI()
        
    def initUI(self):
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.pushButton_2.clicked.connect(self.run)
        self.table_cols = ['검색한 시간', '지역명','온도','날씨']
        self.tableWidget.horizontalHeader().setStretchLastSection(True)        
        self.set_table()
        
    def run(self):
        keyword=self.lineEdit.text()
        print(keyword)
        self.set_table()
        
    def set_table(self):
        #if data:
            row_idx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_idx)
            
            col_idx = self.table_cols.index('검색한 시간')
            #table_item = QtWidgets.QTableWidgetItem(data[''])
            #self.tableWidget.setItem(row_idx,col_idx, table_item)
            
            col_idx = self.table_cols.index('지역명')
            #table_item = QtWidgets.QTableWidgetItem(data[''])
            #self.tableWidget.setItem(row_idx,col_idx, table_item)

            col_idx = self.table_cols.index('온도')
            #table_item = QtWidgets.QTableWidgetItem(data[''])
            #self.tableWidget.setItem(row_idx,col_idx, table_item)

            col_idx = self.table_cols.index('날씨')
            #table_item = QtWidgets.QTableWidgetItem(data[''])
            #self.tableWidget.setItem(row_idx,col_idx, table_item)


            self.tableWidget.horizontalHeader().setStretchLastSection(False)
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            
            #for col_idx in range(self.tableWidget.columnCount()):
               # self.tableWidget.item(row_idx,col_idx).setTextAlignment(Qt.AlignCenter)
            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()