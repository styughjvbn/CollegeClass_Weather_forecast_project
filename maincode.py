from urllib.parse import urlencode, unquote
import requests
import json
import datetime
import sys 
from PyQt5 import QtCore, QtWidgets, uic 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate, Qt

form_class =uic.loadUiType("app.ui")[0]
x=69
y=106
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('날씨 출력 프로그램')
        self.setWindowIcon(QIcon('weather.png'))
        self.date = QDate.currentDate()
        self.initUI()
        self.weather=" "
        self.dt_now = datetime.datetime.now()
        self.keyword=" "
        self.temp=" "
        
    def initUI(self):
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.pushButton_2.clicked.connect(self.run)
        self.table_cols = ['검색한 시간', '지역명','온도','습도','날씨']
        self.tableWidget.horizontalHeader().setStretchLastSection(True)        
        
    def run(self):
        self.keyword=self.lineEdit.text()
        self.set_key()
        self.set_table()
        
    def set_table(self):
        #if data:
        row_idx = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_idx)
            
        col_idx = self.table_cols.index('검색한 시간')
        table_item = QtWidgets.QTableWidgetItem(str(self.dt_now.hour)+":"+str(self.dt_now.minute))
        self.tableWidget.setItem(row_idx,col_idx, table_item)
        
        col_idx = self.table_cols.index('지역명')
        table_item = QtWidgets.QTableWidgetItem(self.keyword)
        self.tableWidget.setItem(row_idx,col_idx, table_item)

        col_idx = self.table_cols.index('온도')
        table_item = QtWidgets.QTableWidgetItem(self.temp)
        self.tableWidget.setItem(row_idx,col_idx, table_item)
        
        col_idx = self.table_cols.index('습도')
        table_item = QtWidgets.QTableWidgetItem(self.mos)
        self.tableWidget.setItem(row_idx,col_idx, table_item)

        col_idx = self.table_cols.index('날씨')
        table_item = QtWidgets.QTableWidgetItem(self.weather)
        self.tableWidget.setItem(row_idx,col_idx, table_item)


        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
            
            #for col_idx in range(self.tableWidget.columnCount()):
               # self.tableWidget.item(row_idx,col_idx).setTextAlignment(Qt.AlignCenter)
            
    def set_key(self):
        if self.keyword=="상당구":
            x=69
            y=106
        elif self.keyword=="서원구":
            x=69
            y=107
        elif self.keyword=="흥덕구":
            x=67
            y=106
        elif self.keyword=="청원구":
            x=69
            y=107
        else:
            print("없습니다. ")
            x=00
            y=00
        
        date=str(self.dt_now.date())
        year=date[:4]
        month=date[5:7]
        day=date[8:10]
        basedate=year+month+day
        time=str(self.dt_now.time())
        hour=int(time[:2])
        minute=int(time[3:5])
        if minute<int(30) :
            hour=str(hour-1)
        minute="30"
        basetime=str(hour)+minute
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst"
        queryString = "?" + urlencode(
        {
            "ServiceKey": unquote("b58MyDUhHqCfbct6sxlCYnyzG6uSiFf8ZDeZXXvrZHLQSYT3zSL3SbOehZ60ZiNiny%2BZpsMSN4PuC59%2BtHvH%2BQ%3D%3D"),
            "base_date": basedate,
            "base_time": basetime,
            "nx": x,
            "ny": y,
            "numOfRows": "36",
            "pageNo": 1,
            "dataType": "JSON"
        }
        )
        queryURL = url + queryString
        response = requests.get(queryURL)

        r_dict = json.loads(response.text)
        r_response = r_dict.get("response")
        r_body = r_response.get("body")
        r_items = r_body.get("items")
        r_item = r_items.get("item")
        for item in r_item:
            if(item.get("category") == "PTY"):
                pty=item.get("fcstValue")#pty=강수형태
                break
        
        for item in r_item:
            if(item.get("category") == "SKY"):
                sky=item.get("fcstValue")#sky=하늘상태
                break
        
        for item in r_item:
            if(item.get("category") == "T1H"):
                self.temp=item.get("fcstValue")#temp=기온
                break
        
        for item in r_item:
            if(item.get("category") == "REH"):
                self.mos=item.get("fcstValue")#mos=습도
                break

        weather_dic={0:"없음",1:"비",2:"짓눈개비",3:"눈",4:"소나기",5:"빗방울",6:"빗방울/눈날림",7:"눈날림"}
        sky_dic={1:"맑음",3:"구름많음",4:"흐림"}
        if int(pty)==0:
            self.weather=sky_dic.get(int(sky))
        else:
            self.weather=weather_dic.get(int(pty))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
