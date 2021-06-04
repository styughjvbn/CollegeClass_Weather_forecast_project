from urllib.parse import urlencode, unquote
import requests
import json
import datetime
import sys 
from PyQt5 import QtCore, QtWidgets, uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate, Qt
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Embedding, LSTM, GRU, Dense, Dropout
from keras.callbacks import EarlyStopping
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.font_manager._rebuild()
from matplotlib import font_manager, rc
from keras.optimizers import Adam
from keras.preprocessing import sequence

form_class =uic.loadUiType("app2.ui")[0]

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
        self.mos=" "
        self.PT=0
        self.weather_image=QIcon('weather.png')
        self.food=""
        self.file=[]
        
    def initUI(self):
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run2)
        self.pushButton_4.clicked.connect(self.update_graph)
        self.table_cols = ['검색한 시간', '지역명','온도','습도','날씨']
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  
        self.tableWidget.cellClicked.connect(self.set_label)
        self.radioButton_3.toggled.connect(self.on_clicked)
        self.radioButton_4.toggled.connect(self.on_clicked1)
        self.radioButton_5.toggled.connect(self.on_clicked2)
        self.radioButton_6.toggled.connect(self.on_clicked3)
        self.pushButton_5.clicked.connect(self.choise_file)
        self.pushButton_6.clicked.connect(self.create_model)
        self.progressBar_2.setValue(0)
        self.progressBar_2.setAlignment(Qt.AlignCenter)
        self.pushButton_7.clicked.connect(self.choise_model)
        
    def run(self):
        self.keyword=self.lineEdit.text()
        self.set_key()
        self.set_table()
    
    def choise_model(self):
        self.textBrowser.clear()
        name=QFileDialog.getExistingDirectory()
        self.file=str(name)
        self.textBrowser.append("선택 모델 : "+self.file+"\n\n")
   
    def choise_file(self):
        name=QFileDialog.getOpenFileNames(self)
        a=1
        for num in name[0]:
            self.textBrowser_2.append(str(a)+"번째 파일 : "+str(num)+"\n\n")
            self.file.append(str(num))   
            a=a+1
            
    def create_model(self):
        start=0
        self.keyword=self.lineEdit_3.text()
        if len(self.file)==2:
            for num in self.file:
                if num[-3:]=="csv":
                    start=start+1
        else:
            self.textBrowser_3.append("선택된 파일의 수가 올바르지 않습니다.\n")
                
        if start==2:
            self.create_model_run()
        else :
            self.textBrowser_3.append("올바르지 않은 확장자의 파일을 선택하였습니다.\n")
            
    def create_model_run(self):
        Train_XSet = pd.read_csv(self.file[0],
                                  names=['기온', '강수량', '풍속', '습도', '이슬점', '기압', '시정']);
        Train_YSet = pd.read_csv(self.file[1],
                                  names=['기온', '강수량', '풍속', '습도', '이슬점', '기압', '시정']);
        X_Train_Set = Train_XSet
        Y_Train_Set = Train_YSet
        self.progressBar_2.setValue(10)

# 데이터 가공하기

#########################################################################
#  이제 여기서부터는 신경망 만들기
#########################################################################
# 모델 구조 설계
        Weather_Forecast_Model = Sequential();

# 최초 입력층


# 은닉층 이름이 달라야 추가된다. 같은 것을 계속 추가할 수는 없다.
# 중간에 ReLU층이 어느 정도 있어야 한다.
        Hidden_Layer1 = Dense(14, input_dim=7,activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer1);
        self.progressBar_2.setValue(20)
        Hidden_Layer2 = Dense(14, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer2);
        self.progressBar_2.setValue(30)
        Hidden_Layer3 = Dense(7, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer3);
        self.progressBar_2.setValue(40)
        Hidden_Layer4 = Dense(7, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer4);
        self.progressBar_2.setValue(50)
        Hidden_Layer5 = Dense(7, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer5);
        Hidden_Layer6 = Dense(7, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer6);
        Hidden_Layer7 = Dense(7, activation='linear');
        Weather_Forecast_Model.add(Hidden_Layer7);


#########################################################################
#  환경설정 및 학습시작
#########################################################################

# 모델 환경설정
        Weather_Forecast_Model.compile(loss='mean_squared_logarithmic_error', optimizer='adam', metrics=['accuracy']);

# 모델 학습하기
        self.progressBar_2.setValue(70)
# 자동종료 함수
        early_stopping = EarlyStopping(monitor='loss', patience=100);
        Weather_Forecast_Model.fit(X_Train_Set,Y_Train_Set, epochs=500, batch_size=500, callbacks=[early_stopping]);
#Weather_Forecast_Model.fit(X_Train_Set,Y_Train_Set, epochs=200, batch_size=500);
        self.textBrowser_3.append(str((Weather_Forecast_Model.evaluate(X_Train_Set,Y_Train_Set)[1]))+"\n")

        Test_Forecast_List = Weather_Forecast_Model.predict(X_Train_Set.head(5));

        for i in range(5):
            self.textBrowser_3.append(str(Test_Forecast_List[i])+"\n")


#########################################################################
#  신경망 저장하기
#########################################################################

        answear = "./Models/"+str(self.keyword)+".ann"

# 모델 저장하기
        Weather_Forecast_Model.save(answear);
        Weather_Forecast_Model.summary();  # 이게 있어야 불러올 때 잘 온다.
        self.progressBar_2.setValue(100)
        self.textBrowser_3.append(str(self.keyword)+".ann 저장 완료\n\n")
        
    def set_label(self, row, column):
        a = self.tableWidget.item(row,2)
        b = self.tableWidget.item(row,4)
        a1 = a.text()
        b1=b.text()

        if b1!="맑음" and b1!="구름많음" and b1!="흐림":
            self.on_clicked2()
        elif int(a1)>=23:
            self.on_clicked()
        elif int(a1)<=10:
            self.on_clicked1()
        
    def set_table(self):
        #if data:
        
        self.dt_now = datetime.datetime.now()
        row_idx = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_idx)
            
        col_idx = self.table_cols.index('검색한 시간')
        table_item = QtWidgets.QTableWidgetItem(str(self.dt_now.hour)+":"+str(self.dt_now.minute)+":"+str(self.dt_now.second))
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
        table_item = QtWidgets.QTableWidgetItem(self.weather_image,self.weather)
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
        self.dt_now = datetime.datetime.now()
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

        weather_dic={0:"없음",1:"비",2:"짓눈개비",3:"눈",4:"소나기",5:"보슬비",6:"보슬비/눈날림",7:"눈날림"}
        weather_icon={0:" ",1:"rain1.png",2:"rain2.png",3:"rain3.png",4:"rain4.png",5:"rain5.png",6:"rain6.png",7:"rain7.png"}
        sky_dic={1:"맑음",3:"구름많음",4:"흐림"}
        sky_icon={1:"sun1.png",3:"sun3.png",4:"sun4.png"}
        if int(pty)==0:
            self.weather=sky_dic.get(int(sky))
            icon=sky_icon.get(int(sky))
            self.weather_image=QIcon("./icon/"+icon)
        else:
            self.weather=weather_dic.get(int(pty))
            icon=weather_icon.get(int(pty))
            self.weather_image=QIcon("./icon/"+icon)
            
            
    def on_clicked(self):
        image=QPixmap("./image/image1.png")
        self.label_5.move(0,60)
        self.label_5.setPixmap(image)
    def on_clicked1(self):
        image=QPixmap("./image/image2.png")
        self.label_5.move(0,60)
        self.label_5.setPixmap(image)
    def on_clicked2(self):
        image=QPixmap("./image/image3.png")
        self.label_5.move(0,60)
        self.label_5.setPixmap(image)
    def on_clicked3(self):
        image=QPixmap("./image/image4.png")
        self.label_5.move(0,60)
        self.label_5.setPixmap(image)
        
    def update_graph(self):
        plt.rc('font', family='Malgun Gothic')

        food1 = pd.read_excel('foods.xlsx', sheet_name='Hot day')
        food2 = pd.read_excel('foods.xlsx', sheet_name='Cold day')
        food3 = pd.read_excel('foods.xlsx', sheet_name='rainy,snowy day')
        food4 = pd.read_excel('foods.xlsx', sheet_name='Dusty day')
        
        plt.figure(1)
        ratio1 = food1['num']
        lables1 = food1['food']
        explode1 = [0.10,0.03,0.03,0.05,0.08]
        colors1 = ['gold', 'whitesmoke', 'whitesmoke','brown', 'silver']
        title1 = '[더운 날 선호도 음식 TOP5]'
        plt.title(title1)
        plt.pie(ratio1, labels=lables1, autopct='%.1f%%', startangle=260, counterclock =False, explode = explode1, shadow =True, colors=colors1)
        plt.ioff()
        plt.savefig('./image/image1.png')
        
        plt.figure(2)
        ratio2 = food2['num']
        lables2 = food2['food']
        explode2 = [0.08,0.10,0.05,0.03,0.03]
        colors2 = ['silver', 'gold', 'brown','whitesmoke', 'whitesmoke']
        title2 = '[추운 날 선호도 음식 TOP5]'
        plt.title(title2)
        plt.pie(ratio2, labels=lables2, autopct='%.1f%%', startangle=260, counterclock =False, explode = explode2, shadow =True, colors=colors2)
        plt.ioff()
        plt.savefig('./image/image2.png')

        plt.figure(3)
        ratio3 = food3['num']
        lables3 = food3['food']
        explode3 = [0.08,0.10,0.03,0.03,0.05]
        colors3 = ['silver', 'gold', 'whitesmoke','whitesmoke', 'brown']
        title3 = '[비/눈 오는 날 선호도 음식 TOP5]'
        plt.title(title3)
        plt.pie(ratio3, labels=lables3, autopct='%.1f%%', startangle=260, counterclock =False, explode = explode3, shadow =True, colors=colors3)
        plt.ioff()
        plt.savefig('./image/image3.png')
        
        plt.figure(4)
        ratio4 = food4['num']
        lables4 = food4['food']
        explode4 = [0.03,0.05,0.10,0.03,0.08]
        colors4 = ['whitesmoke', 'brown', 'gold','whitesmoke', 'silver']
        title4 = '[미세먼지 많은 날 선호도 음식 TOP5]'
        plt.title(title4)
        plt.pie(ratio4, labels=lables4, autopct='%.1f%%', startangle=260, counterclock =False, explode = explode4, shadow =True, colors=colors4)
        plt.ioff()
        plt.savefig('./image/image4.png')
        
    def run2(self):
        self.PT=self.lineEdit_2.text()
        answear =self.file
        
        Weather_Forecast_Model = load_model(answear);
        Weather_Forecast_Model.summary();
        answear = "./Work/PD.csv"
        X_data = pd.read_csv(answear, names=['기온', '강수량', '풍속', '습도', '이슬점', '기압', '시정']);
        # 앞으로의 예측시간
        Time_Hour = self.PT
        Time_Hour = int(Time_Hour);
        # 데이터 가공
        #X_data.iloc[0,0] = X_data.iloc[0,0] * 0.1;
        X_data.iloc[0, 3] = X_data.iloc[0, 3] * 0.01;
        #X_data.iloc[0,4] = X_data.iloc[0,4] * 0.1;
        X_data.iloc[0, 5] = (X_data.iloc[0, 5] - 1000);
        X_data.iloc[0, 6] = X_data.iloc[0, 6] * 0.01;

        Temp = Weather_Forecast_Model.predict(X_data);

        time = 0;
        while(time < Time_Hour - 1):
            Temp = Weather_Forecast_Model.predict(Temp);
            time = time + 1;

        # 데이터 가공 및 결과 받아오기
        self.Forecast_Temperature = Temp[0][0];

        # 1미만이면 그냥 없는 것으로 하자 0으로 나눔 예외발생한다.
        if Temp[0][1] < 1:
            self.Forecast_Rain = 0;
        else:
            self.Forecast_Rain = Temp[0][1];
        self.Forecast_Wind = Temp[0][2];
        self.Forecast_Humidity = Temp[0][3] * 100;
        self.Forecast_Dew_Point = Temp[0][4];
        self.Forecast_Pressure = (Temp[0][5]) + 1000;
        self.Forecast_Sight = Temp[0][6] * 1000;
        self.set_text()
        

    def set_text(self):
        self.textBrowser.append("기상예보 ")
        self.textBrowser.append("예측 시간:"+str(self.PT)+"시간 후\n\n")
        self.textBrowser.append("기온: "+str(self.Forecast_Temperature)+"C")
        self.textBrowser.append("강수량: "+ str(self.Forecast_Rain)+ "mm")
        self.textBrowser.append("풍속: "+str(self.Forecast_Wind)+"M/s")
        self.textBrowser.append("습도: "+ str(self.Forecast_Humidity)+ "%")
        self.textBrowser.append("이슬점: "+ str(self.Forecast_Dew_Point)+ "C")
        self.textBrowser.append("기압: "+ str(self.Forecast_Pressure)+ "hpa")
        self.textBrowser.append("시정: "+ str(self.Forecast_Sight )+"Meter")  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()