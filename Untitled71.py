#!/usr/bin/env python
# coding: utf-8

# In[22]:


from bs4 import BeautifulSoup
from PIL import ImageTk, Image  
from decimal import Decimal
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np
import lxml
import tweepy
import webbrowser
import time
import json
import requests
import threading
import concurrent.futures
from functools import partial


# In[2]:


def connectToSQL():
    mydb = mysql.connector.connect(    
          host="remotemysql.com",
          user="YtOwo2nL4F",
          password="wt77a2Odny",
          database="YtOwo2nL4F",
          charset = "utf8mb4")
    
    return mydb
    #cursor = mydb.cursor(buffered=True)
    
def connectToMongoDB():
    import pymongo
    from pymongo import MongoClient
    cluster = MongoClient("mongodb+srv://PohJingHong:Hachiman1!@cluster0.uqvf0.mongodb.net/UserReportedNews?retryWrites=true&w=majority")
    
    return cluster

def connectToTwitterAPI():
    consumer_key = "29phws1YVdhkX3HuN1s51S013"
    consumer_secret = "Zn8jMgsu1tMUFnvtpXUKisLFvpP3CX6LRD7Xq4AOKc8KmsKBkV"
    callback_url = "oob"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    redirect_url = auth.get_authorization_url()
    print(redirect_url)

    code_website = requests.get(redirect_url).text
    user_pint_input = input("What's the pin value?")
    auth.get_access_token(user_pint_input)
    #user account
    api = tweepy.API(auth) 
    
    return api

cluster = connectToMongoDB()
api = connectToTwitterAPI()

#choose database
db = cluster["UserReportedNews"] 
#choose collection
collection = db['News'] 


# In[ ]:


def connectToSQL():
    mydb = mysql.connector.connect(    
          host="remotemysql.com",
          user="YtOwo2nL4F",
          password="wt77a2Odny",
          database="YtOwo2nL4F",
          charset = "utf8mb4")
    
    return mydb
    #cursor = mydb.cursor(buffered=True)


# In[23]:


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_LoginWindow(object):
    
    def setupUi(self, LoginWindow):
        self.window = QtWidgets.QMainWindow()
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #Contain the rest of widgets
        self.LoginWidget = QtWidgets.QWidget(self.centralwidget)
        self.LoginWidget.setGeometry(QtCore.QRect(60, 30, 701, 431))
        self.LoginWidget.setObjectName("LoginWidget")
        
        #Label at left side
        self.LabelLeft = QtWidgets.QLabel(self.LoginWidget)
        self.LabelLeft.setGeometry(QtCore.QRect(0, 0, 361, 431))
        self.LabelLeft.setStyleSheet("border-top-left-radius: 50px;\n"
"border-bottom-left-radius: 50px;\n"
"border-image: url(../../../../../../Poh Jing Hong/New folder/Pictures/Camera Roll/眼镜雪乃.jpg);")
        self.LabelLeft.setText("")
        self.LabelLeft.setScaledContents(True)
        self.LabelLeft.setObjectName("LabelLeft")
        
        #Label at right side
        self.LabelRight = QtWidgets.QLabel(self.LoginWidget)
        self.LabelRight.setGeometry(QtCore.QRect(360, 0, 351, 431))
        self.LabelRight.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border-image:url(../../../../../../Poh Jing Hong/New folder/Pictures/Camera Roll/wp2137415-oregairu-wallpapers (4).jpg);\n"
"border-bottom-right-radius: 50px;\n"
"border-top-right-radius: 50px;")
        self.LabelRight.setText("")
        self.LabelRight.setObjectName("LabelRight")
        
        #'Log In' label
        self.LoginLabel = QtWidgets.QLabel(self.LoginWidget)
        self.LoginLabel.setGeometry(QtCore.QRect(500, 40, 81, 61))   
        font = QtGui.QFont()
        font.setFamily("Niagara Engraved")
        font.setPointSize(30)
        font.setUnderline(True)
        self.LoginLabel.setFont(font)
        self.LoginLabel.setObjectName("LoginLabel")
        
        #Username entry
        self.username = QtWidgets.QLineEdit(self.LoginWidget)
        self.username.setGeometry(QtCore.QRect(410, 150, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.username.setFont(font)
        self.username.setStyleSheet("background-color:rgb(23, 201, 255);\n"
"border-bottom-color:rgba(0,0,0,0);\n"
"color:rgb(255, 255, 255);\n"
"padding-bottom: 7px;\n"
"border-top-left-radius: 10px;\n"
"border-bottom-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"\n"
"")
        self.username.setObjectName("username")
        
        #Password entry
        self.password = QtWidgets.QLineEdit(self.LoginWidget)
        self.password.setGeometry(QtCore.QRect(410, 210, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color:rgb(23, 201, 255);\n"
"border-bottom-color:rgba(0,0,0,0);\n"
"color:rgb(255, 255, 255);\n"
"padding-bottom: 7px;\n"
"border-top-left-radius: 10px;\n"
"border-bottom-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"\n"
"")
        self.password.setObjectName("password")
        
        #Login Button
        self.LoginButton = QtWidgets.QPushButton(self.LoginWidget)
        self.LoginButton.setGeometry(QtCore.QRect(450, 300, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LoginButton.setFont(font)
        self.LoginButton.setStyleSheet("border-top-left-radius: 10px;\n"
"border-bottom-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"color:rgb(255, 255, 255);\n"
"background-color:rgb(85, 170, 255);")
        self.LoginButton.setObjectName("LoginButton")
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        
        #self.LoginButton.clicked.connect( lambda:(threading.Thread(target=self.validateUser).start()) )
        self.LoginButton.clicked.connect(self.runLongTask)
        
    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "MainWindow"))
        self.LoginLabel.setText(_translate("LoginWindow", "Log In"))
        #self.username.setText(_translate("LoginWindow", "  Username:"))
        #self.password.setText(_translate("LoginWindow", "  Password:"))
        self.LoginButton.setText(_translate("LoginWindow", "Login"))

    
    def validateUser2(self,paws):
        
        passwd_of_user = "Password123!"
            
        if passwd_of_user == "":
            print("Please enter username")
                #messagebox.showerror("Error", "The user information is incorrect")
        
        
        if(passwd_of_user == paws and paws != ""):
            self.window = QtWidgets.QMainWindow()#create a main window
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.window)#put the UI of homepage to main window created just now
            self.window.show()
    
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect( partial(self.worker.run, username = str(self.username.text()),password = str(self.password.text())))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.validateUser2)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.LoginButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.LoginButton.setEnabled(True)
        )
    
   
    def login_window(self):
        import sys
        self.app = QtWidgets.QApplication(sys.argv)
        self.LoginWindow = QtWidgets.QMainWindow()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self.LoginWindow)
        self.LoginWindow.show()
        sys.exit(self.app.exec_())


# In[24]:


content = ""
result = ""


# In[28]:


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1012, 719)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AppWidget = QtWidgets.QWidget(self.centralwidget)
        self.AppWidget.setGeometry(QtCore.QRect(40, 20, 891, 621))
        self.AppWidget.setObjectName("AppWidget")
        self.frame = QtWidgets.QFrame(self.AppWidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 891, 621))
        self.frame.setStyleSheet("QPushButton{\n"
"    \n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color:rgb(175, 211, 237);\n"
"\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.HomeFrame = QtWidgets.QFrame(self.frame)
        self.HomeFrame.setGeometry(QtCore.QRect(0, 0, 891, 80))
        self.HomeFrame.setStyleSheet("background-color:rgb(249, 249, 249);\n"
"border-top-left-radius: 50px;\n"
"border-top-right-radius:50px;\n"
"")
        self.HomeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.HomeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.HomeFrame.setObjectName("HomeFrame")
        self.greetingLabel = QtWidgets.QLabel(self.HomeFrame)
        self.greetingLabel.setGeometry(QtCore.QRect(40, 20, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.greetingLabel.setFont(font)
        self.greetingLabel.setAutoFillBackground(False)
        self.greetingLabel.setStyleSheet("background-color:rgb(249, 249, 249);\n"
"")
        self.greetingLabel.setObjectName("greetingLabel")
        self.clock = QtWidgets.QTimeEdit(self.HomeFrame)
        self.clock.setGeometry(QtCore.QRect(720, 20, 121, 41))
        self.clock.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border-color:rgb(0, 0, 0);")
        self.clock.setObjectName("clock")
        self.ContentFrame = QtWidgets.QFrame(self.frame)
        self.ContentFrame.setGeometry(QtCore.QRect(150, 80, 741, 541))
        self.ContentFrame.setStyleSheet("QFrame{\n"
"border :2px solid ;\n"
"border-top-color: rgb(255, 255, 255);\n"
"border-bottom-right-radius: 50px;\n"
"border-image:url(../../../../../../Poh Jing Hong/New folder/Pictures/Camera Roll/istockphoto-1135638647-170667a.jpg);\n"
"background-color:rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.ContentFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ContentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ContentFrame.setObjectName("ContentFrame")
        self.tagLabel = QtWidgets.QLabel(self.ContentFrame)
        self.tagLabel.setGeometry(QtCore.QRect(480, 50, 221, 401))
        self.tagLabel.setStyleSheet("border-image:none;\n"
"border:1px solid white;\n"
"border-bottom-right-radius: 0px;\n"
"background-color: rgba(0, 255, 255, 0)")
        self.tagLabel.setText("")
        self.tagLabel.setObjectName("tagLabel")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.ContentFrame)
        self.verticalScrollBar.setGeometry(QtCore.QRect(700, 50, 21, 401))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.label_3 = QtWidgets.QLabel(self.ContentFrame)
        self.label_3.setGeometry(QtCore.QRect(110, 50, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border-image:none;\n"
"border:none;\n"
"border-bottom-right-radius: 0px;\n"
"background-color: rgba(0, 255, 255, 0)")
        self.label_3.setObjectName("label_3")
        self.tweetsSearch = QtWidgets.QLineEdit(self.ContentFrame)
        self.tweetsSearch.setGeometry(QtCore.QRect(70, 150, 191, 31))
        self.tweetsSearch.setObjectName("tweetsSearch")
        self.pushButton = QtWidgets.QPushButton(self.ContentFrame)
        self.pushButton.setGeometry(QtCore.QRect(270, 150, 91, 31))
        self.pushButton.setStyleSheet("border:none;\n"
"background-color: rgba(0, 255, 255, 20)")
        self.pushButton.setObjectName("pushButton")
        self.rumourPercent = QtWidgets.QLCDNumber(self.ContentFrame)
        self.rumourPercent.setGeometry(QtCore.QRect(70, 260, 241, 101))
        self.rumourPercent.setStyleSheet("border-image:none;\n"
"border:2px solid;\n"
"\n"
"border-bottom-right-radius: 0px;\n"
"background-color: rgba(0, 255, 255, 0)")
        self.rumourPercent.setObjectName("rumourPercent")
        self.rumourPercent.display("99.00")
        self.MenuBar = QtWidgets.QFrame(self.frame)
        self.MenuBar.setGeometry(QtCore.QRect(0, 80, 151, 541))
        self.MenuBar.setStyleSheet("QFrame{\n"
"    background-color:rgb(205, 226, 243);\n"
"    \n"
"    border-bottom-left-radius: 50px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color:rgb(175, 211, 237);\n"
"    border-top-left-radius: 50px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    border-radius : 10px;\n"
"    background-color:rgb(243, 248, 252);\n"
"    margin:1px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.MenuBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MenuBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MenuBar.setObjectName("MenuBar")
        self.HomeButton = QtWidgets.QPushButton(self.MenuBar)
        self.HomeButton.setGeometry(QtCore.QRect(0, 0, 151, 40))
        self.HomeButton.setMinimumSize(QtCore.QSize(0, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.HomeButton.setFont(font)
        self.HomeButton.setStyleSheet("margin-top:3px;\n"
"")
        self.HomeButton.setAutoDefault(False)
        self.HomeButton.setDefault(False)
        self.HomeButton.setFlat(False)
        self.HomeButton.setObjectName("HomeButton")
        self.NewsButton = QtWidgets.QPushButton(self.MenuBar)
        self.NewsButton.setGeometry(QtCore.QRect(0, 40, 151, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.NewsButton.setFont(font)
        self.NewsButton.setObjectName("NewsButton")
        self.HistoryButton = QtWidgets.QPushButton(self.MenuBar)
        self.HistoryButton.setGeometry(QtCore.QRect(0, 80, 151, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.HistoryButton.setFont(font)
        self.HistoryButton.setObjectName("HistoryButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.RumourPercent_thread)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.greetingLabel.setText(_translate("MainWindow", "    Welcome, Poh Jing Hong"))
        self.label_3.setText(_translate("MainWindow", "  Check Tweets for Rumour"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.HomeButton.setText(_translate("MainWindow", "Home"))
        self.NewsButton.setText(_translate("MainWindow", "News Acticles"))
        self.HistoryButton.setText(_translate("MainWindow", "History"))


 
    def getRumourPercentage(self,search_content,search_result):
        
        
        global api
        global cluster
        
        #self.tweetsSearch
        #self.rumourPercent
        
        if "https://twitter.com/" in search_content.text():
        
            hashtag_dict = {}
            db = cluster["Tweets"] #choose database
            collection = db['TweetHashtag'] #choose collection
        
            query = list(collection.find().sort("count",-1))
        
            for i in range(len(query)):
                hashtag_dict[query[i]['hashtag']] = query[i]['count']
                print(hashtag_dict[query[i]['hashtag']])
        
            url = search_content.text()
            entry = url.split("/")
        
            tweets_id = entry[5]
            result = api.get_status(tweets_id, tweet_mode = "extended")
        
            json_str = json.dumps(result._json)
            data = json.loads(json_str)
        
            entry = data["full_text"]
        
            entry = entry.split(" ")
            
            for i in range(len(entry)):                
                if "https:" in entry[i]:
                    entry[i] = " "
                 
            entry = " ".join(entry)
            print("this is entry:"+entry)
            
            #return entry
            search_result.display((ConvertDataAndPredict(entry))) #set the result on QLCDNumber
   
   # def displayPredictResult(self,entry):
   #     self.rumourPercent.display((ConvertDataAndPredict(entry))) #set the result on QLCDNumber


        #self.tweetsSearch
        #self.rumourPercent
    def RumourPercent_thread(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(partial(self.worker.run_RumourPercent,tweetsSearch = self.tweetsSearch,rumourPercent = self.rumourPercent))
        self.worker.predict_finished.connect(self.thread.quit)
        self.worker.predict_finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.predict_progress.connect(self.displayPredictResult)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.pushButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pushButton.setEnabled(True)
        )
        
    def homepage_window(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


# In[31]:


from PyQt5.QtCore import QObject, QThread, pyqtSignal
# Snip...

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    
    predict_finished = pyqtSignal()
    predict_progress = pyqtSignal(str)
    
    #def run(self):
    def run(self,username,password):
        usr = "1"
        paws = "Password123!"
        
        print("username:"+usr)
        print("password:"+paws)
        
        sql_dbs = connectToSQL()
        cursor = sql_dbs.cursor(buffered=True)
        
        passwd_of_user=""
            
        try:
            cursor.execute("select password from USER where username = {}".format(("'"+usr+"'")))
            for i in cursor:
                passwd_of_user = i[0]
                print("passwd_of_user: ",passwd_of_user)
                self.progress.emit(passwd_of_user)
            
        #if the username is not found in the database    
        except mysql.connector.ProgrammingError as err:
            #messagebox.showerror("Error", "The user is not exist")
            print("The user is not exist")
            
        self.finished.emit()
    
    
    def run_RumourPercent(self,tweetsSearch,rumourPercent):
        homepage = Ui_MainWindow()

        homepage.getRumourPercentage(tweetsSearch,rumourPercent)
        #self.predict_progress.emit()
        self.predict_finished.emit()
        


# In[7]:


from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from num2words import num2words
import re

newcorpus = []
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def ConvertData(pdata):

    newcorpus = []
    for i in range(len(pdata)):

        review = re.sub('[^a-zA-Z0-9]', ' ', pdata[i])
        review = review.lower()
        review = review.split()#split store into list
    
        review = [num2words(review[i]) if review[i].isdigit() else review[i] for i in range(len(review))  ]
        review = [word for word in review if not word in stopwords.words()]
        review = [lemmatizer.lemmatize(word) for word in review]
        review = [ps.stem(word) for word in review ]

        #turn list to string
        review = ' '.join(review)
    
        newcorpus.append(review)
        
    return newcorpus


# In[8]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
#Thread pool executors, less code than type manually
import concurrent.futures

#Turn both of these into threads
import threading
import time


df =pd.read_csv("C:/Users/Public/Documents/SIM/New folder/project_redo/tweetsdata.csv",header = None)

db = cluster["UserReportedNews"] 
#choose collection/tables
collection = db['News']

if collection.find().count()>0:
    print("Hi")
    list_cur = list(collection.find())
    new = pd.DataFrame(list_cur)
    
    lst = list(ConvertData(new["title"]))
                           
    lst2 = list(new["TrueFalse"])
    update_data = pd.DataFrame(list(zip(lst, lst2)),columns =['content', 'label'])
    update_data["label"].replace({"True": "0", "False":"1"},inplace=True)
    df = pd.concat([df, update_data.rename(columns={'content':0,'label':1})],axis= 0,ignore_index=True)

    
df = df.sample(frac =.50)
df.reset_index(inplace=True)

df = df[[0,1]]
y = df[1].astype(np.uint8)

corpus = []

for i in range(len(df)):
    corpus.append(df[0][i])
    
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Transforming text... = ", current_time)

## TFidf Vectorizer
tfidf_v=TfidfVectorizer(max_features=30000,ngram_range=(1,2))

X=tfidf_v.fit_transform(corpus).toarray()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Done! =", current_time)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Training the model... =", current_time)

## Divide the dataset into Train and Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)
multinomial = MultinomialNB(alpha = 0.1)
multinomial.fit(X_train, y_train)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Done! =", current_time)


# In[9]:


def addingRows(collection):
    
    print("Hi")
    list_cur = list(collection.find())
    new = pd.DataFrame(list_cur)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        lst = list(executor.map((ConvertData, new["title"])))
    #lst = list(ConvertData(new["title"]))
    lst2 = list(new["TrueFalse"])
    update_data = pd.DataFrame(list(zip(lst, lst2)),columns =['content', 'label'])
    update_data["label"].replace({"True": "0", "False":"1"},inplace=True)
    df = pd.concat([df, update_data.rename(columns={'content':0,'label':1})],axis= 0,ignore_index=True)

    return df


# In[10]:


tfidf_test=TfidfVectorizer(max_features=30000,ngram_range=(1,2),vocabulary = tfidf_v.vocabulary_)

def ConvertDataAndPredict(pdata):

    if pdata.strip() == "":
        predict_result = 0
        predict_result = "{result}".format(result = predict_result)
        
    else:
        global tfidf_test
        
        newcorpus = []
        for i in range(1):

            review = re.sub('[^a-zA-Z0-9]', ' ', pdata)
            review = review.lower()
            review = review.split()#split store into list
    
            review = [num2words(review[i]) if review[i].isdigit() else review[i] for i in range(len(review))  ]
            review = [word for word in review if not word in stopwords.words()]
            review = [lemmatizer.lemmatize(word) for word in review]
            review = [ps.stem(word) for word in review ]

            #turn list to string
            review = ' '.join(review)
    
            newcorpus.append(review)

        X_tes=tfidf_test.fit_transform(newcorpus).toarray()
    
        predict_result = multinomial.predict_proba(X_tes)
        predict_result = round(predict_result[0][1] * 100, 2)
    
        predict_result = "{result}".format(result = predict_result)
        
    return predict_result


# In[32]:


if __name__ == '__main__':    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    #sys.exit(app.exec_())
    app.exec_()
    del app


# In[ ]:





# In[ ]:




