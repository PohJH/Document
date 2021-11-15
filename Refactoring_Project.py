#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
import mysql.connector


# In[ ]:


def connectToSQL():
    mydb = mysql.connector.connect(    
          host="remotemysql.com",
          user="YtOwo2nL4F",
          password="wt77a2Odny",
          database="YtOwo2nL4F",
          charset = "utf8mb4")
    
    return mydb

    
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

#Twitter api
api = connectToTwitterAPI()

#MongoDB
cluster = connectToMongoDB()
db = cluster["UserReportedNews"] #choose database
collection = db['News'] #choose collection

#MySQL
cursor = connectToSQL().cursor(buffered=True)

#connect to NewsApi
from newsapi import NewsApiClient 
newsapi = NewsApiClient(api_key="a2221ecba1104192a83c8fe6d7bce4cd")


# In[ ]:


class Tweets:
    
    global api
    
    def getPopularTopic(self,tagLabel):
        trends = api.trends_place(1)
        data = trends[0] 
        trend = data['trends']
        names = [i['name'] for i in trend]
        names = '\n'.join(names[0:20])
        tagLabel.setText(names)

var = {}


# In[ ]:


class History:
    
    def clicked(self,url):
        if(url != ""):
            webbrowser.open(url)
    
    def share_to_twitter(self,accuracy,url):
    
        image = Image.open('C:/Poh Jing Hong/New folder/Pictures/Camera Roll/sharetotwitter.jpg')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial', 50)
        draw.text((320, 100),accuracy, font=font, fill=(48, 97, 97))
        #draw.text((170, 90),accuracy , fill="blue",size = "100",font = font)
        image_edited = image.save('C:/Poh Jing Hong/New folder/Pictures/Camera Roll/sharetotwitter_edited.png')
    
        media = api.media_upload('C:/Poh Jing Hong/New folder/Pictures/Camera Roll/sharetotwitter_edited.png')
    
        post_result = api.update_status("The rumour percentage of Tweets:"+ str(url), media_ids=[media.media_id])
    
        print("Posted")
        
    def showHistory(self,frame):
    
        mydb = connectToSQL()
        cursor = mydb.cursor(buffered=True)
        #cursor.execute("select DetectedNews, DetectedUrl, DetectedAccuracy from HISTORY where username = {} ".format("'"+str("1")+"'"))
        cursor.execute("select DetectedNews, DetectedUrl, DetectedAccuracy from HISTORY where username = 1 ")   

        arr_len = (len(list(cursor)))
        
        arrContent = [None] * arr_len
        arrURL = [None] * arr_len
        arrPercent = [None] * arr_len
        arrShare = [None] * arr_len    

        print('arr:',len(arrContent))
        count = 0
        
        cursor.execute("select DetectedNews, DetectedUrl, DetectedAccuracy from HISTORY where username = 1 ")
        for i in cursor:
            print('arr:',len(arrContent))
            print(count)
            arrContent[count] = QtWidgets.QPushButton(frame)
            arrContent[count].setGeometry(QtCore.QRect(0, 0+(count*50), 221, 50))
            arrContent[count].setStyleSheet("border:1px solid;\n" 
                                                "background-color:rgba(0,255,255,70)")      
                
            arrURL[count] = QtWidgets.QPushButton(frame)      
            arrURL[count].setGeometry(QtCore.QRect(220, 0+(count*50), 361, 50))
            arrURL[count].setStyleSheet("border:1px solid;\n" 
                                            "background-color:rgba(0,255,255,50)")
            
            arrPercent[count] = QtWidgets.QPushButton(frame) 
            arrPercent[count].setGeometry(QtCore.QRect(580, 0+(count*50), 50, 50))
            arrPercent[count].setStyleSheet("border:1px solid;\n" 
                                            "background-color:rgba(0,255,255,30)")
            
            arrShare[count] = QtWidgets.QPushButton(frame)
            arrShare[count].setGeometry(QtCore.QRect(630, 0+(count*50), 50, 50))
            arrShare[count].setStyleSheet("border:1px solid;\n"
                                          "background-color:rgba(0,255,255,10)")   
            
            arrContent[count].setText(i[0])
            arrURL[count].setText(i[1])
            arrPercent[count].setText(i[2])
            arrShare[count].setText('Share')
            
            arrURL[count].clicked.connect(partial(self.clicked, url = i[1]))
            arrShare[count].clicked.connect(partial(self.share_to_twitter,accuracy = i[2],url = i[1] ))
            
            arrContent[count].show()
            arrURL[count].show()
            arrPercent[count].show()
            arrShare[count].show()
             
            print(i[0])
            count += 1
        


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:



        


# In[ ]:


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_LoginWindow(object):
    
    def __init__(self, LoginWindow):
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
        
        LoginWindow.setWindowTitle("MainWindow")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.LoginLabel.setText("Log In")
        self.LoginButton.setText("Login")

        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        
        #self.LoginButton.clicked.connect( lambda:(threading.Thread(target=self.validateUser).start()) )
        self.LoginButton.clicked.connect(self.runLongTask)

        
    def validateUser(self,paws):
        
        print('Here')
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
        self.worker.progress.connect(self.validateUser)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.LoginButton.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.LoginButton.setEnabled(True)
        )


# In[ ]:


from functools import partial
class NewsApi:
    
    def clicked(self,url):
        if(url != ""):
            webbrowser.open(url)

    #show the news of selected category
    def changeCategories(self,frame,comboBox):
        combo_box_text = str(comboBox.currentText()) #Get the current text of combo box
        print(combo_box_text)
        self.showNews(frame,combo_box_text)
      
        
    def showNews(self,frame,category):
        
        #The connection with News Api
        global newsapi

        print(category)
        #The amount of news retrieve
        pagesize = 20
        var = newsapi.get_top_headlines(category=category,language='en',page_size=pagesize )

        arr = [None] * pagesize #To store the QPushButton
        
        for i in range(pagesize): 
            articles = var['articles'][i]['url'] #url of news
            title = var['articles'][i]['title'] #title of news
            arr[i] = QtWidgets.QPushButton(frame)
            arr[i].setText(title)
            arr[i].clicked.connect(partial(self.clicked, url=articles)) #pop up the website of news
            arr[i].setGeometry(QtCore.QRect(0, 0+(i*30), 561, 28))
            self.pushButton_3 = QtWidgets.QPushButton(frame)
            self.pushButton_3.setGeometry(QtCore.QRect(620, 0, 61, 28))
            font = QtGui.QFont()
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            font.setStrikeOut(False)
            self.pushButton_3.setFont(font)
            self.pushButton_3.setStyleSheet("border:none;\n"
                "background-color:rgb(255, 0, 0)")
            self.pushButton_3.setObjectName("pushButton_3")
            self.pushButton_5 = QtWidgets.QPushButton(frame)
            self.pushButton_5.setGeometry(QtCore.QRect(560, 0, 61, 28))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_5.setFont(font)
            self.pushButton_5.setStyleSheet("border:none;\n"
            "background-color:rgb(170, 255, 127);\n"
            "")
            self.pushButton_5.setDefault(False)
            self.pushButton_5.setFlat(False)
            self.pushButton_5.setObjectName("pushButton_5")
        

            arr[i].show()
        #self.news.setGeometry(QtCore.QRect(20, 60, 681, 28))
        
        #ContentFrame.show()
        
    def displayNews(self,var,frame):
        print("Here")
        pagesize = 20
        arr = [None] * pagesize #To store the QPushButton
        
        for i in range(pagesize): 
            articles = var['articles'][i]['url'] #url of news
            title = var['articles'][i]['title'] #title of news
            arr[i] = QtWidgets.QPushButton(frame)
            arr[i].setText(title)
            arr[i].clicked.connect(partial(self.clicked, url=articles)) #pop up the website of news
            arr[i].setGeometry(QtCore.QRect(0, 0+(i*30), 561, 28))
            self.pushButton_3 = QtWidgets.QPushButton(frame)
            self.pushButton_3.setGeometry(QtCore.QRect(620, 0, 61, 28))
            font = QtGui.QFont()
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            font.setStrikeOut(False)
            self.pushButton_3.setFont(font)
            self.pushButton_3.setStyleSheet("border:none;\n"
                "background-color:rgb(255, 0, 0)")
            self.pushButton_3.setObjectName("pushButton_3")
            self.pushButton_5 = QtWidgets.QPushButton(frame)
            self.pushButton_5.setGeometry(QtCore.QRect(560, 0, 61, 28))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_5.setFont(font)
            self.pushButton_5.setStyleSheet("border:none;\n"
            "background-color:rgb(170, 255, 127);\n"
            "")
            self.pushButton_5.setDefault(False)
            self.pushButton_5.setFlat(False)
            self.pushButton_5.setObjectName("pushButton_5")
            arr[i].show()


# In[ ]:



from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    
    def setupUi(self, MainWindow):
        
        self.homepage = HomePage()
        self.newspage = NewsPage()
        self.historypage = HistoryPage()
        topic = Tweets()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1012, 719)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AppWidget = QtWidgets.QWidget(self.centralwidget)
        self.AppWidget.setGeometry(QtCore.QRect(40, 20, 891, 621))
        self.AppWidget.setObjectName("AppWidget")
        self.Mainframe = QtWidgets.QFrame(self.AppWidget)
        self.Mainframe.setGeometry(QtCore.QRect(0, 0, 891, 621))
        self.Mainframe.setStyleSheet("QPushButton{\n"
"    \n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color:rgb(175, 211, 237);\n"
"\n"
"}")
        self.Mainframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Mainframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Mainframe.setObjectName("frame")
        self.HomeFrame = QtWidgets.QFrame(self.Mainframe)
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
        self.ContentFrame = QtWidgets.QFrame(self.Mainframe)
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

        self.MenuBar = QtWidgets.QFrame(self.Mainframe)
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
        
        MainWindow.setWindowTitle("MainWindow")
        self.greetingLabel.setText("    Welcome, Poh Jing Hong")
        self.HomeButton.setText("Home")
        self.NewsButton.setText("News Acticles")
        self.HistoryButton.setText("History")
 
        #self.pushButton.clicked.connect(self.RumourPercent_thread)
        self.HomeButton.clicked.connect(partial(self.homepage.Window1, Mainframe =self.Mainframe))
        self.NewsButton.clicked.connect(partial(self.newspage.Window2, Mainframe =self.Mainframe, NewsButton = self.NewsButton ))
        self.HistoryButton.clicked.connect(partial(self.historypage.Window3, Mainframe = self.Mainframe))
        


   
   # def displayPredictResult(self,entry):
   #     self.rumourPercent.display((ConvertDataAndPredict(entry))) #set the result on QLCDNumber



# In[ ]:


class HomePage:

    def Window1(self,Mainframe):
        print("Window1")
        topic = Tweets()

        self.ContentFrame = QtWidgets.QFrame(Mainframe)
        self.ContentFrame.setGeometry(QtCore.QRect(150, 80, 741, 541))
        #self.ContentFrame.setGeometry(QtCore.QRect(150, 80, 741, 541))
        
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
        
        self.tagLabel.setObjectName("tagLabel")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.ContentFrame)
        self.verticalScrollBar.setGeometry(QtCore.QRect(700, 50, 21, 401))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalScrollBar.setStyleSheet("background-color:rgba(0,255,255,0)")
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
        self.rumourPercent.display("0.00")
           
        topic.getPopularTopic(self.tagLabel)
        self.label_3.setText("  Check Tweets for Rumour")
        self.pushButton.setText("Submit")
        self.pushButton.clicked.connect(self.RumourPercent_thread)
        self.ContentFrame.show()
        
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
            
        #Thread to predict the result of Tweets  
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


# In[ ]:


class NewsPage:

    def Window2(self,Mainframe,NewsButton):

        newsApi = NewsApi() #Instance of class NewsApi
   #--------------------------------------------------------------------------------------------     
        print("WIndow2")
        
        self.ContentFrame = QtWidgets.QFrame(Mainframe)
        self.ContentFrame.setGeometry(QtCore.QRect(150, 80, 741, 541))
        font = QtGui.QFont()
        font.setPointSize(2)
        self.ContentFrame.setFont(font)
        self.ContentFrame.setStyleSheet("#ContentFrame{\n"
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
        
        #-------------------------------------------------------------------------------------
        self.verticalScrollBar = QtWidgets.QScrollBar(self.ContentFrame)
        self.verticalScrollBar.setGeometry(QtCore.QRect(700, 60, 21, 431))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalScrollBar.setStyleSheet("background-color:rgba(0,255, 255, 0)")
        
        #self.news = QtWidgets.QPushButton(self.ContentFrame)
        #self.news.setGeometry(QtCore.QRect(20, 60, 681, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        self.comboBox_2 = QtWidgets.QComboBox(self.ContentFrame)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 30, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("business")
        self.comboBox_2.addItem("entertainment")
        self.comboBox_2.addItem("general")
        self.comboBox_2.addItem("health")
        self.comboBox_2.addItem("science")
        self.comboBox_2.addItem("sports")
        self.comboBox_2.addItem("technology")

        self.frame = QtWidgets.QFrame(self.ContentFrame)
        self.frame.setGeometry(QtCore.QRect(20, 60, 681, 431))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.frame.raise_()

        #newsApi.showNews(self.frame,'business')
        #self.scrollAreaWidgetContents
        #newsApi.showNews(self.frame,'business')
        self.LoadNews_thread(self.frame, 'business')
        
        #newsApi.displayNews(self.frame)
        self.comboBox_2.activated.connect(partial(newsApi.changeCategories,frame=self.frame,comboBox=self.comboBox_2))
        
        self.ContentFrame.show()

        
    
    #Thread to predict the result of Tweets  
    def LoadNews_thread(self,Frame,Category):
        
        newsApi = NewsApi() 
        
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(partial(self.worker.run_NewsPage,frame = Frame,category = Category))
        self.worker.load_news_progress.connect(partial(newsApi.displayNews, frame = Frame))
        self.worker.load_news_finished.connect(self.thread.quit)
        self.worker.load_news_finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        #NewsButton.setEnabled(False)
        #self.thread.finished.connect(
        #    lambda: NewsButton.setEnabled(True)
        #)


# In[ ]:


class HistoryPage:

    def Window3(self,Mainframe):
        print("Window3")
        history = History() # aggregate History
        
        self.ContentFrame = QtWidgets.QFrame(Mainframe)
        self.ContentFrame.setGeometry(QtCore.QRect(150, 80, 741, 541))
        font = QtGui.QFont()
        font.setPointSize(2)
        self.ContentFrame.setFont(font)
        self.ContentFrame.setStyleSheet("#ContentFrame{\n"
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
        
        self.HistoryscrollArea = QtWidgets.QScrollArea(self.ContentFrame)
        self.HistoryscrollArea.setGeometry(QtCore.QRect(20, 60, 701, 431))
        self.HistoryscrollArea.setStyleSheet("\n"
"background-color: rgba(0, 255,  255,0);\n"
"border:none;")
        self.HistoryscrollArea.setWidgetResizable(True)
        self.HistoryscrollArea.setObjectName("HistoryscrollArea")
        self.HistoryscrollAreaWidgetContents = QtWidgets.QWidget()
        self.HistoryscrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 701, 431))
        self.HistoryscrollAreaWidgetContents.setObjectName("HistoryscrollAreaWidgetContents")
        self.HistoryScrollBar = QtWidgets.QScrollBar(self.HistoryscrollAreaWidgetContents)
        self.HistoryScrollBar.setGeometry(QtCore.QRect(680, 0, 21, 431))
        self.HistoryScrollBar.setStyleSheet("background-color:rgba(0,255,255,0);")
        self.HistoryScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.HistoryScrollBar.setObjectName("HistoryScrollBar")
        
        #--------------------------------------------------------------------------------
        """
        self.content_del = QtWidgets.QPushButton(self.HistoryscrollAreaWidgetContents)
        self.content_del.setGeometry(QtCore.QRect(0, 0, 221, 51))
        self.content_del.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,70)")
        self.content_del.setText("")
        self.content_del.setObjectName("content_del")
        self.url_del = QtWidgets.QPushButton(self.HistoryscrollAreaWidgetContents)
        self.url_del.setGeometry(QtCore.QRect(220, 0, 361, 51))
        self.url_del.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,50)")
        self.url_del.setText("")
        self.url_del.setObjectName("url_del")
        self.percent_del = QtWidgets.QLabel(self.HistoryscrollAreaWidgetContents)
        self.percent_del.setGeometry(QtCore.QRect(580, 0, 51, 51))
     
        #------------------------------------------------------------------------------------
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.percent_del.setFont(font)
        self.percent_del.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,30)")
        self.percent_del.setText("")
        self.percent_del.setObjectName("percent_del")
        self.share_del = QtWidgets.QLabel(self.HistoryscrollAreaWidgetContents)
        self.share_del.setGeometry(QtCore.QRect(630, 0, 51, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.share_del.setFont(font)
        self.share_del.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,10)")
        self.share_del.setText("")
        self.share_del.setObjectName("share_del")
        
        """
        self.HistoryscrollArea.setWidget(self.HistoryscrollAreaWidgetContents)
        self.HistoryContent = QtWidgets.QLabel(self.ContentFrame)
        self.HistoryContent.setGeometry(QtCore.QRect(20, 20, 221, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.HistoryContent.setFont(font)
        self.HistoryContent.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,70)")
        self.HistoryContent.setObjectName("HistoryContent")
        self.HistoryURL = QtWidgets.QLabel(self.ContentFrame)
        self.HistoryURL.setGeometry(QtCore.QRect(240, 20, 361, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.HistoryURL.setFont(font)
        self.HistoryURL.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,50)")
        self.HistoryURL.setObjectName("HistoryURL")
        self.HistoryPercent = QtWidgets.QLabel(self.ContentFrame)
        self.HistoryPercent.setGeometry(QtCore.QRect(600, 20, 51, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.HistoryPercent.setFont(font)
        self.HistoryPercent.setStyleSheet("border:1px solid;\n"
"background-color:rgba(0,255,255,30)")
        self.HistoryPercent.setObjectName("HistoryPercent")
        self.ContentFrame.show()
        
        self.HistoryContent.setText("Content")
        self.HistoryURL.setText("URL")
        self.HistoryPercent.setText("%")
        
        history.showHistory(self.HistoryscrollAreaWidgetContents)


# In[ ]:


from PyQt5.QtCore import QObject, QThread, pyqtSignal
# Snip...

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    
    predict_finished = pyqtSignal()
    predict_progress = pyqtSignal(str)
    
    load_news_progress = pyqtSignal(dict)
    load_news_finished = pyqtSignal()
    
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
        homepage = HomePage()

        homepage.getRumourPercentage(tweetsSearch,rumourPercent)
        #self.predict_progress.emit()
        self.predict_finished.emit()
        
    def run_NewsPage(self,frame,category):
    
        global newsapi
        print(category)
        #The amount of news retrieve
        pagesize = 20
        time.sleep(10)
        var = newsapi.get_top_headlines(category=category,language='en',page_size=pagesize )  
        
        self.load_news_progress.emit(var)
        self.load_news_finished.emit()
   


# In[ ]:





# In[ ]:


global newsapi
var = newsapi.get_top_headlines(category='business',language='en',page_size=20 )  
type(var)


# In[ ]:


if __name__ == '__main__':    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    
    page = Ui_LoginWindow(LoginWindow)
    LoginWindow.show()
    
    app.exec_()
    del app


# In[ ]:


self.tagLabel = QtWidgets.QLabel(self.ContentFrame)
self.tagLabel.setGeometry(QtCore.QRect(480, 50, 221, 401))
self.tagLabel.setStyleSheet("border-image:none;\n"
"border:1px solid white;\n"
"border-bottom-right-radius: 0px;\n"
"background-color: rgba(0, 255, 255, 0)")

self.tagLabel.setObjectName("tagLabel")
self.verticalScrollBar = QtWidgets.QScrollBar(self.ContentFrame)
self.verticalScrollBar.setGeometry(QtCore.QRect(700, 50, 21, 401))
self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
self.verticalScrollBar.setObjectName("verticalScrollBar")
self.verticalScrollBar.setStyleSheet("background-color:rgba(0,255,255,0)")
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
self.rumourPercent.display("0.00")




topic.getPopularTopic(self.tagLabel)
self.pushButton.clicked.connect(self.RumourPercent_thread)
self.HomeButton.clicked.connect(partial(self.homepage.Window1, Mainframe =self.Mainframe))
self.NewsButton.clicked.connect(self.newspage.Window2)
self.HistoryButton.clicked.connect(self.historypage.Window3)
self.retranslateUi(MainWindow)
QtCore.QMetaObject.connectSlotsByName(MainWindow)


# In[ ]:




