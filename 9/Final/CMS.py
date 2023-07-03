from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import ast
import re
import json
import requests
from bs4 import BeautifulSoup

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(524, 641)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_find = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_find.setGeometry(QtCore.QRect(110, 440, 311, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_find.setFont(font)
        self.pushButton_find.setStyleSheet("")
        self.pushButton_find.setObjectName("pushButton_find")
        self.pushButton_change = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_change.setGeometry(QtCore.QRect(110, 100, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.pushButton_change.setFont(font)
        self.pushButton_change.setStyleSheet("")
        self.pushButton_change.setObjectName("pushButton_change")
        self.pushButton_contacts = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_contacts.setGeometry(QtCore.QRect(110, 180, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.pushButton_contacts.setFont(font)
        self.pushButton_contacts.setStyleSheet("")
        self.pushButton_contacts.setObjectName("pushButton_contacts")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 400, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_txt = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_txt.setGeometry(QtCore.QRect(110, 300, 150, 71))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.pushButton_txt.setFont(font)
        self.pushButton_txt.setStyleSheet("")
        self.pushButton_txt.setObjectName("pushButton_txt")
        self.label_done = QtWidgets.QLabel(self.centralwidget)
        self.label_done.setGeometry(QtCore.QRect(430, 330, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_done.setFont(font)
        self.label_done.setText("")
        self.label_done.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_done.setWordWrap(True)
        self.label_done.setObjectName("label_done")
        self.pushButton_web = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_web.setGeometry(QtCore.QRect(110, 510, 311, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_web.setFont(font)
        self.pushButton_web.setStyleSheet("")
        self.pushButton_web.setObjectName("pushButton_web")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 270, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.pushButton_json = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_json.setGeometry(QtCore.QRect(270, 300, 150, 71))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.pushButton_json.setFont(font)
        self.pushButton_json.setStyleSheet("")
        self.pushButton_json.setObjectName("pushButton_json")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 524, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_change, self.pushButton_contacts)
        MainWindow.setTabOrder(self.pushButton_contacts, self.pushButton_txt)
        MainWindow.setTabOrder(self.pushButton_txt, self.pushButton_json)
        MainWindow.setTabOrder(self.pushButton_json, self.pushButton_find)
        MainWindow.setTabOrder(self.pushButton_find, self.pushButton_web)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main"))
        self.label.setText(_translate("MainWindow", "Contacts Manager System:"))
        self.pushButton_find.setText(_translate("MainWindow", "Find Contact Name and Phone"))
        self.pushButton_change.setText(_translate("MainWindow", "Change Contacts"))
        self.pushButton_contacts.setText(_translate("MainWindow", "Contacts List"))
        self.label_2.setText(_translate("MainWindow", "Faz 1:"))
        self.label_3.setText(_translate("MainWindow", "Faz 2:"))
        self.pushButton_txt.setText(_translate("MainWindow", "TXT"))
        self.pushButton_web.setText(_translate("MainWindow", "Web Scraping"))
        self.label_4.setText(_translate("MainWindow", "Save As:"))
        self.pushButton_json.setText(_translate("MainWindow", "JSON"))

class Ui_Change(object):
    def setupUi(self, Change):
        Change.setObjectName("Change")
        Change.resize(524, 514)
        self.pushButton = QtWidgets.QPushButton(Change)
        self.pushButton.setGeometry(QtCore.QRect(360, 420, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(Change)
        self.label_4.setGeometry(QtCore.QRect(20, 300, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Change)
        self.label_5.setGeometry(QtCore.QRect(20, 340, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.lineEdit_phone = QtWidgets.QLineEdit(Change)
        self.lineEdit_phone.setGeometry(QtCore.QRect(140, 340, 361, 30))
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.lineEdit_id = QtWidgets.QLineEdit(Change)
        self.lineEdit_id.setGeometry(QtCore.QRect(140, 180, 271, 30))
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.lineEditName = QtWidgets.QLineEdit(Change)
        self.lineEditName.setGeometry(QtCore.QRect(140, 220, 361, 30))
        self.lineEditName.setObjectName("lineEditName")
        self.label_6 = QtWidgets.QLabel(Change)
        self.label_6.setGeometry(QtCore.QRect(20, 180, 121, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.radioButton = QtWidgets.QRadioButton(Change)
        self.radioButton.setGeometry(QtCore.QRect(20, 70, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Change)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 100, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit_Family = QtWidgets.QLineEdit(Change)
        self.lineEdit_Family.setGeometry(QtCore.QRect(140, 260, 361, 30))
        self.lineEdit_Family.setObjectName("lineEdit_Family")
        self.radioButton_3 = QtWidgets.QRadioButton(Change)
        self.radioButton_3.setGeometry(QtCore.QRect(20, 130, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_2 = QtWidgets.QLabel(Change)
        self.label_2.setGeometry(QtCore.QRect(20, 220, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Change)
        self.label_3.setGeometry(QtCore.QRect(20, 260, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(Change)
        self.label.setGeometry(QtCore.QRect(10, 10, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_email = QtWidgets.QLineEdit(Change)
        self.lineEdit_email.setGeometry(QtCore.QRect(140, 300, 361, 30))
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.label_errorshow = QtWidgets.QLabel(Change)
        self.label_errorshow.setGeometry(QtCore.QRect(20, 380, 481, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_errorshow.setFont(font)
        self.label_errorshow.setText("")
        self.label_errorshow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_errorshow.setWordWrap(True)
        self.label_errorshow.setObjectName("label_errorshow")
        self.pushButton_open = QtWidgets.QPushButton(Change)
        self.pushButton_open.setGeometry(QtCore.QRect(420, 180, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_open.setFont(font)
        self.pushButton_open.setObjectName("pushButton_open")

        self.retranslateUi(Change)
        QtCore.QMetaObject.connectSlotsByName(Change)
        Change.setTabOrder(self.radioButton, self.radioButton_2)
        Change.setTabOrder(self.radioButton_2, self.radioButton_3)
        Change.setTabOrder(self.radioButton_3, self.lineEdit_id)
        Change.setTabOrder(self.lineEdit_id, self.pushButton_open)
        Change.setTabOrder(self.pushButton_open, self.lineEditName)
        Change.setTabOrder(self.lineEditName, self.lineEdit_Family)
        Change.setTabOrder(self.lineEdit_Family, self.lineEdit_email)
        Change.setTabOrder(self.lineEdit_email, self.lineEdit_phone)
        Change.setTabOrder(self.lineEdit_phone, self.pushButton)

    def retranslateUi(self, Change):
        _translate = QtCore.QCoreApplication.translate
        Change.setWindowTitle(_translate("Change", "Dialog"))
        self.pushButton.setText(_translate("Change", "Add"))
        self.label_4.setText(_translate("Change", "Email Address:"))
        self.label_5.setText(_translate("Change", "Phone Number:"))
        self.label_6.setText(_translate("Change", "Id Sort by Name:"))
        self.radioButton.setText(_translate("Change", "Add"))
        self.radioButton_2.setText(_translate("Change", "Remove"))
        self.radioButton_3.setText(_translate("Change", "Change"))
        self.label_2.setText(_translate("Change", "Name:"))
        self.label_3.setText(_translate("Change", "Family Name:"))
        self.label.setText(_translate("Change", "What do you want to do ?"))
        self.pushButton_open.setText(_translate("Change", "open"))

class Ui_List(object):
    def setupUi(self, List):
        List.setObjectName("List")
        List.resize(524, 641)
        self.textBrowser = QtWidgets.QTextBrowser(List)
        self.textBrowser.setGeometry(QtCore.QRect(10, 95, 501, 531))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(List)
        self.label.setGeometry(QtCore.QRect(10, 10, 400, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.radioButton_Family = QtWidgets.QRadioButton(List)
        self.radioButton_Family.setGeometry(QtCore.QRect(180, 60, 121, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_Family.setFont(font)
        self.radioButton_Family.setObjectName("radioButton_Family")
        self.radioButton_name = QtWidgets.QRadioButton(List)
        self.radioButton_name.setGeometry(QtCore.QRect(80, 60, 88, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_name.setFont(font)
        self.radioButton_name.setChecked(True)
        self.radioButton_name.setObjectName("radioButton_name")
        self.label_2 = QtWidgets.QLabel(List)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(List)
        QtCore.QMetaObject.connectSlotsByName(List)
        List.setTabOrder(self.radioButton_name, self.radioButton_Family)
        List.setTabOrder(self.radioButton_Family, self.textBrowser)

    def retranslateUi(self, List):
        _translate = QtCore.QCoreApplication.translate
        List.setWindowTitle(_translate("List", "Dialog"))
        self.label.setText(_translate("List", "Contacts List:"))
        self.radioButton_Family.setText(_translate("List", "Family Name"))
        self.radioButton_name.setText(_translate("List", "Name"))
        self.label_2.setText(_translate("List", "Sort:"))

class Ui_Texts(object):
    def setupUi(self, Texts):
        Texts.setObjectName("Texts")
        Texts.resize(524, 641)
        self.textBrowser = QtWidgets.QTextBrowser(Texts)
        self.textBrowser.setGeometry(QtCore.QRect(20, 390, 491, 231))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Texts)
        self.pushButton.setGeometry(QtCore.QRect(370, 300, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Texts)
        self.label.setGeometry(QtCore.QRect(20, 10, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Texts)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 491, 231))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(Texts)
        self.label_2.setGeometry(QtCore.QRect(20, 350, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Texts)
        QtCore.QMetaObject.connectSlotsByName(Texts)
        Texts.setTabOrder(self.textEdit, self.pushButton)
        Texts.setTabOrder(self.pushButton, self.textBrowser)

    def retranslateUi(self, Texts):
        _translate = QtCore.QCoreApplication.translate
        Texts.setWindowTitle(_translate("Texts", "Dialog"))
        self.pushButton.setText(_translate("Texts", "Find"))
        self.label.setText(_translate("Texts", "Enter Text:"))
        self.label_2.setText(_translate("Texts", "Names and Phone Numbers:"))

class Ui_web(object):
    def setupUi(self, web):
        web.setObjectName("web")
        web.resize(524, 425)
        self.lineEdit_email = QtWidgets.QLineEdit(web)
        self.lineEdit_email.setGeometry(QtCore.QRect(140, 170, 361, 30))
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.pushButton = QtWidgets.QPushButton(web)
        self.pushButton.setGeometry(QtCore.QRect(360, 330, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(web)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.lineEdit_Family = QtWidgets.QLineEdit(web)
        self.lineEdit_Family.setGeometry(QtCore.QRect(140, 130, 361, 30))
        self.lineEdit_Family.setObjectName("lineEdit_Family")
        self.label_3 = QtWidgets.QLabel(web)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.lineEdit_phone = QtWidgets.QLineEdit(web)
        self.lineEdit_phone.setGeometry(QtCore.QRect(140, 210, 361, 30))
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.label_errorshow = QtWidgets.QLabel(web)
        self.label_errorshow.setGeometry(QtCore.QRect(20, 250, 491, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_errorshow.setFont(font)
        self.label_errorshow.setText("")
        self.label_errorshow.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_errorshow.setWordWrap(True)
        self.label_errorshow.setObjectName("label_errorshow")
        self.label_4 = QtWidgets.QLabel(web)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(web)
        self.label_5.setGeometry(QtCore.QRect(20, 210, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.lineEditName = QtWidgets.QLineEdit(web)
        self.lineEditName.setGeometry(QtCore.QRect(140, 90, 361, 30))
        self.lineEditName.setObjectName("lineEditName")
        self.label = QtWidgets.QLabel(web)
        self.label.setGeometry(QtCore.QRect(10, 20, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(web)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 330, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(web)
        QtCore.QMetaObject.connectSlotsByName(web)
        web.setTabOrder(self.lineEditName, self.lineEdit_Family)
        web.setTabOrder(self.lineEdit_Family, self.lineEdit_email)
        web.setTabOrder(self.lineEdit_email, self.lineEdit_phone)
        web.setTabOrder(self.lineEdit_phone, self.pushButton_2)
        web.setTabOrder(self.pushButton_2, self.pushButton)

    def retranslateUi(self, web):
        _translate = QtCore.QCoreApplication.translate
        web.setWindowTitle(_translate("web", "Web Scraping"))
        self.pushButton.setText(_translate("web", "Add"))
        self.label_2.setText(_translate("web", "Name:"))
        self.label_3.setText(_translate("web", "Family Name:"))
        self.label_4.setText(_translate("web", "Email Address:"))
        self.label_5.setText(_translate("web", "Phone Number:"))
        self.label.setText(_translate("web", "Click to get data from site:"))
        self.pushButton_2.setText(_translate("web", "Get Data"))

class CMS(Ui_MainWindow):
    def __init__(self):
        global myGlist
        myGlist = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def Load(self):
        global myGlist
        try:
            contactsFile = open("MyContact.txt", "r")
            for i in contactsFile.readlines():
                myGlist.append(ast.literal_eval(i))
            contactsFile.close()
        except:
            contactsFile = open("MyContact.txt", "w")
            contactsFile.write("\n".join(myGlist))
            contactsFile.close()
            myGlist = []

    def ChangeContacts(self):
        self.label_done.setText("")
        global myGlist
        appC = QtWidgets.QDialog()
        GUIC = Ui_Change()
        GUIC.setupUi(appC)

        myList = myGlist
        myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]

        def email(email_address):
            if email_address == "":
                return True
            else:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9]+[.][a-z0-9]{2,3}$'

                if re.search(regex, email_address):
                    return True
                else:
                    return False

        def saveClicked():
            global myGlist
            myList = myGlist
            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]

            GUIC.label_errorshow.setText("")

            if GUIC.radioButton.isChecked():
                if email(GUIC.lineEdit_email.text().lower()) == True:
                    adder = {'Name: ': GUIC.lineEditName.text().capitalize(),
                             'Family Name: ': GUIC.lineEdit_Family.text().capitalize(),
                             'Email Address: ': GUIC.lineEdit_email.text(),
                             'Phone Number: ': GUIC.lineEdit_phone.text()
                             }

                    myList.append(adder)
                    GUIC.lineEdit_id.setText("")
                    GUIC.lineEditName.setText("")
                    GUIC.lineEdit_Family.setText("")
                    GUIC.lineEdit_email.setText("")
                    GUIC.lineEdit_phone.setText("")

                else:
                    GUIC.label_errorshow.setText("Email Address is invalid !")

            elif GUIC.radioButton_2.isChecked():
                if GUIC.lineEdit_id.text().isdigit() == False:
                    GUIC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif GUIC.lineEdit_id.text() == "":
                    GUIC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(GUIC.lineEdit_id.text()) < len(myList):
                    GUIC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    del myList[int(GUIC.lineEdit_id.text())]
                    GUIC.lineEdit_id.setText("")
                    GUIC.lineEditName.setText("")
                    GUIC.lineEdit_Family.setText("")
                    GUIC.lineEdit_email.setText("")
                    GUIC.lineEdit_phone.setText("")

            elif GUIC.radioButton_3.isChecked():
                if GUIC.lineEdit_id.text().isdigit() == False:
                    GUIC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif GUIC.lineEdit_id.text() == "":
                    GUIC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(GUIC.lineEdit_id.text()) < len(myList):
                    GUIC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    if email(GUIC.lineEdit_email.text().lower()) == True:
                        myList[int(GUIC.lineEdit_id.text())] = {'Name: ': GUIC.lineEditName.text().capitalize(),
                                 'Family Name: ': GUIC.lineEdit_Family.text().capitalize(),
                                 'Email Address: ': GUIC.lineEdit_email.text(),
                                 'Phone Number: ': GUIC.lineEdit_phone.text()
                                 }

                        GUIC.lineEdit_id.setText("")
                        GUIC.lineEditName.setText("")
                        GUIC.lineEdit_Family.setText("")
                        GUIC.lineEdit_email.setText("")
                        GUIC.lineEdit_phone.setText("")

                    else:
                        GUIC.label_errorshow.setText("Email Address is invalid !")

            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]
            myGlist = myList

        def add():
            GUIC.lineEdit_id.setEnabled(False)
            GUIC.pushButton_open.setEnabled(False)
            GUIC.pushButton.setText("Add")

        def remove():
            GUIC.lineEdit_id.setEnabled(True)
            GUIC.pushButton_open.setEnabled(True)
            GUIC.pushButton.setText("Remove")

        def change():
            GUIC.lineEdit_id.setEnabled(True)
            GUIC.pushButton_open.setEnabled(True)
            GUIC.pushButton.setText("Change")

        def open():
            global myGlist
            myList = myGlist
            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]

            GUIC.label_errorshow.setText("")
            id = GUIC.lineEdit_id.text()

            if id != "":
                if GUIC.lineEdit_id.text().isdigit() == False:
                    GUIC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif GUIC.lineEdit_id.text() == "":
                    GUIC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(GUIC.lineEdit_id.text()) < len(myList):
                    GUIC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    GUIC.lineEditName.setText(myList[int(id)]["Name: "])
                    GUIC.lineEdit_Family.setText(myList[int(id)]["Family Name: "])
                    GUIC.lineEdit_email.setText(myList[int(id)]["Email Address: "])
                    GUIC.lineEdit_phone.setText(myList[int(id)]["Phone Number: "])

            else:
                GUIC.lineEditName.setText("")
                GUIC.lineEdit_Family.setText("")
                GUIC.lineEdit_email.setText("")
                GUIC.lineEdit_phone.setText("")

        GUIC.lineEdit_id.setEnabled(False)
        GUIC.pushButton_open.setEnabled(False)
        GUIC.radioButton.clicked.connect(add)
        GUIC.radioButton_2.clicked.connect(remove)
        GUIC.radioButton_3.clicked.connect(change)
        GUIC.pushButton.clicked.connect(saveClicked)
        GUIC.pushButton_open.clicked.connect(open)

        appC.show()
        appC.exec_()

    def ListContacts(self):
        self.label_done.setText("")
        global myGlist
        appL = QtWidgets.QDialog()
        GUIL = Ui_List()
        GUIL.setupUi(appL)

        myList = myGlist

        def name_sort():
            myList = myGlist
            sort = [i for i in sorted(myList, key=lambda item: item['Name: '])]

            printer = []

            x = 0
            for i in sort:
                temp = []
                for j in list(i.keys()):
                    temp.append(j + i[j])
                printer.append("ID: " + str(x) + ",\n" + ",\n".join(temp))
                x += 1

            GUIL.textBrowser.setText("\n\n".join(printer))

        def family_sost():
            myList = myGlist
            sort = [i for i in sorted(myList, key=lambda item: item['Family Name: '])]

            printer = []

            x = 0
            for i in sort:
                temp = []
                for j in list(i.keys()):
                    temp.append(j + i[j])
                printer.append("ID: " + str(x) + ",\n" + ",\n".join(temp))
                x += 1

            GUIL.textBrowser.setText("\n\n".join(printer))

        name_sort()
        GUIL.radioButton_name.clicked.connect(name_sort)
        GUIL.radioButton_Family.clicked.connect(family_sost)

        appL.show()
        appL.exec_()

    def Web(self):
        self.label_done.setText("")
        global myGlist
        self.label_done.setText("")
        appW = QtWidgets.QDialog()
        GUIW = Ui_web()
        GUIW.setupUi(appW)

        def email(email_address):
            if email_address == "":
                return True
            else:
                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9]+[.][a-z0-9]{2,3}$'

                if re.search(regex, email_address):
                    return True
                else:
                    return False

        def saveClicked():
            global myGlist
            myList = myGlist
            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]

            GUIW.label_errorshow.setText("")

            if email(GUIW.lineEdit_email.text().lower()) == True:
                adder = {'Name: ': GUIW.lineEditName.text().capitalize(),
                         'Family Name: ': GUIW.lineEdit_Family.text().capitalize(),
                         'Email Address: ': GUIW.lineEdit_email.text(),
                         'Phone Number: ': GUIW.lineEdit_phone.text()
                         }

                myList.append(adder)
                GUIW.lineEditName.setText("")
                GUIW.lineEdit_Family.setText("")
                GUIW.lineEdit_email.setText("")
                GUIW.lineEdit_phone.setText("")

            else:
                GUIW.label_errorshow.setText("Email Address is invalid !")

            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]
            myGlist = myList

        def scraping():
            url = "https://www.fakenamegenerator.com/"

            mylist = []

            try:
                HEADERS = ({'User-Agent': 'Mozilla/4.0 (X11; Windows x86_64)'})

                page = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(page.content, "html.parser")

                name = []
                info = []

                for item in soup.select("dl.dl-horizontal"):
                    info.append(item.get_text())

                for item in soup.select("div.address"):
                    name.append(item.get_text())

                email = info[8][:info[8].index("  ")].replace("\nEmail Address\n", "")
                phone = "+" + (info[4].replace("Country code", "") + " " + info[3].replace("Phone", "")).replace("\n", "")

                name = name[0][:name[0].index("\n\n")].replace("\n", "").split()
                fname = " ".join((name[:2]))
                family = name[-1]

                mylist = [fname, family, email, phone]
                return mylist

            except:
                return mylist

        def getData():
            QtWidgets.QApplication.processEvents()
            myList = scraping()
            if myList != []:
                GUIW.label_errorshow.setText("")
                GUIW.lineEditName.setText(myList[0])
                GUIW.lineEdit_Family.setText(myList[1])
                GUIW.lineEdit_email.setText(myList[2])
                GUIW.lineEdit_phone.setText(myList[3])
            else:
                GUIW.label_errorshow.setText("Internet Connection Lost.")

        GUIW.pushButton.clicked.connect(saveClicked)
        GUIW.pushButton_2.clicked.connect(getData)

        appW.show()
        appW.exec_()

    def Text(self):
        self.label_done.setText("")
        appT = QtWidgets.QDialog()
        GUIT = Ui_Texts()
        GUIT.setupUi(appT)

        def NamePhone():
            text = GUIT.textEdit.toPlainText()

            phones = re.findall('[#]+([0-9]+)', text)
            names = re.findall('[@]+([A-Za-z]+)', text)

            if names == []:
                names = ["No names !"]
            if phones == []:
                phones = ["No phones !"]

            printer = "Names:\n" + "\n".join(names) + "\n\nPhones:\n" + "\n".join(phones)

            GUIT.textBrowser.setText(printer)

        GUIT.pushButton.clicked.connect(NamePhone)

        appT.show()
        appT.exec_()

    def TXTfile(self):
        global myGlist
        file = open("MyContact.txt", "w")
        file.write("\n".join([str(i) for i in myGlist]))
        self.label_done.setText("Done")
        file.close()

    def JSONfile(self):
        global myGlist
        file = open("MyContact.json", "w")

        dictionary = {}
        for i in myGlist:
            dictionary[str(myGlist.index(i))] = i
        json.dump(dictionary, file)
        file.close()
        self.label_done.setText("Done")


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

GUI = CMS()
GUI.setupUi(MainWindow)
GUI.Load()

GUI.pushButton_change.clicked.connect(GUI.ChangeContacts)
GUI.pushButton_contacts.clicked.connect(GUI.ListContacts)
GUI.pushButton_txt.clicked.connect(GUI.TXTfile)
GUI.pushButton_json.clicked.connect(GUI.JSONfile)
GUI.pushButton_find.clicked.connect(GUI.Text)
GUI.pushButton_web.clicked.connect(GUI.Web)

MainWindow.show()
sys.exit(app.exec_())
