import json
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree
from Win import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
import sys

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Gui(Ui_MainWindow):
    def __init__(self):
        self.Contacts = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def Tabs(self):
        if self.tabWidget.currentIndex() == 2:
            self.tableWidget.setVisible(False)
            self.label_6.setVisible(False)
            self.pushButton_first.setVisible(False)
            self.pushButton_last.setVisible(False)
        else:
            self.tableWidget.setVisible(True)
            self.label_6.setVisible(True)
            self.pushButton_first.setVisible(True)
            self.pushButton_last.setVisible(True)

    def Theme(self):
        if self.horizontalSlider.value() == 1:
            self.tabWidget.setStyleSheet("background-color:#0E1621; color:#BFFF00")

            # lineEdits
            self.lineEdit_Fname.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_Lname.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_phone.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_email.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_Fname_2.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_Lname_2.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_phone_2.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit_email_2.setStyleSheet("background-color:#0E1621; color:white")
            self.lineEdit.setStyleSheet("background-color:#242F3D;color:#E9E8E8")

            # labels
            self.label.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_2.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_3.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_4.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_5.setStyleSheet("color:white")
            self.label_6.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_7.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_8.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_9.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_10.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_11.setStyleSheet("color:white")
            self.label_12.setStyleSheet("color:white")
            self.label_13.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_14.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_15.setStyleSheet("background-color:#242F3D;color:#E9E8E8")
            self.label_dark.setStyleSheet("background-color:#0E1621; color:#BFFF00")
            self.label_save.setStyleSheet("background-color:#0E1621; color:#BFFF00")

            # table
            self.tableWidget.setStyleSheet("background-color:#242F3D;color:#8D94A6")

            # textEdit
            self.textBrowser.setStyleSheet("background-color:#0E1621; color:white")
            self.textBrowser_2.setStyleSheet("background-color:#0E1621; color:white")
            self.textBrowser_3.setStyleSheet("background-color:#0E1621; color:white")

            # button
            self.pushButton_add.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_update.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_remove.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_first.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_last.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_add_2.setStyleSheet("background-color:#29A0DD; color:white")
            self.pushButton_Find.setStyleSheet("background-color:#29A0DD; color:white")

        else:
            self.tabWidget.setStyleSheet("background-color:white; color:#004242")

            # lineEdits
            self.lineEdit_Fname.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_Lname.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_phone.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_email.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_Fname_2.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_Lname_2.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_phone_2.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit_email_2.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.lineEdit.setStyleSheet("background-color:#F1F1F1;color:#293A4C")

            # labels
            self.label.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_2.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_3.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_4.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_5.setStyleSheet("color:black")
            self.label_6.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_7.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_8.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_9.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_10.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_11.setStyleSheet("color:black")
            self.label_12.setStyleSheet("color:black")
            self.label_13.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_14.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_15.setStyleSheet("background-color:#F1F1F1;color:#293A4C")
            self.label_dark.setStyleSheet("background-color:white; color:#313B4D")
            self.label_save.setStyleSheet("background-color:white; color:#313B4D")

            # table
            self.tableWidget.setStyleSheet("background-color:#F1F1F1;color:black")

            # textEdit
            self.textBrowser.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.textBrowser_2.setStyleSheet("background-color:#BBBBBB; color:#004242")
            self.textBrowser_3.setStyleSheet("background-color:#BBBBBB; color:#004242")

            # button
            self.pushButton_add.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_update.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_remove.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_first.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_last.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_add_2.setStyleSheet("background-color:#318CE7; color:white")
            self.pushButton_Find.setStyleSheet("background-color:#318CE7; color:white")

    def AddContacts(self):
        self.labelError.clear()

        helpValue = True
        Fname = self.lineEdit_Fname.text()
        Lname = self.lineEdit_Lname.text()
        phone = self.lineEdit_phone.text()
        email = self.lineEdit_email.text()


        if Fname == "":
            helpValue = False
            self.labelError.setText("Name is required.")
        elif email == "":
            pass
        elif self.CheckValidEmail(email) == False:
            helpValue = False
            self.labelError.setVisible(True)
            self.labelError.setText("Email Is Not Valid.")

        if helpValue == True:
            self.Contacts.append({
                'Fname': Fname,
                'Lname': Lname,
                'email': email,
                'phone': phone
            })

            self.Table()
            self.Empty()

    def UpdateContacts(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            self.labelError.clear()

            helpValue = True
            Fname = self.lineEdit_Fname.text()
            Lname = self.lineEdit_Lname.text()
            phone = self.lineEdit_phone.text()
            email = self.lineEdit_email.text()


            if Fname == "":
                helpValue = False
                self.labelError.setText("Name is required.")
            elif email == "":
                pass
            elif self.CheckValidEmail(email) == False:
                helpValue = False
                self.labelError.setVisible(True)
                self.labelError.setText("Email Is Not Valid.")

            if helpValue == True:
                self.Contacts[row] = {
                    'Fname': Fname,
                    'Lname': Lname,
                    'email': email,
                    'phone': phone
                }

                self.Table()
                self.Empty()

        else:
            self.labelError.setText("Select a contact from table.")

    def RemoveContacts(self):
        row = self.tableWidget.currentRow()
        if row != -1:
            self.labelError.clear()

            self.Contacts.pop(row)
            self.Table()
            self.Empty()

        else:
            self.labelError.setText("Select a contact from table.")

    def CheckValidEmail(self, email):
        reg = r'^([0-9A-Za-z]|\.|\_|\-)+[@]([0-9A-Za-z]|\_|\-|\.)+[.][A-Za-z]{2,4}$'

        if re.search(reg, email):
            return True
        else:
            return False

    def Table(self, sort=None):
        if sort == "Fname":
            contacts = [i for i in sorted(self.Contacts, key=lambda obj: obj['Fname'])]
        elif sort == "Lname":
            contacts = [i for i in sorted(self.Contacts, key=lambda obj: obj['Lname'])]
        else:
            contacts = self.Contacts

        self.tableWidget.setRowCount(0)

        for i in range(0, len(contacts)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(contacts[i]['Fname']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(contacts[i]['Lname']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(contacts[i]['phone']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(contacts[i]['email']))

    def LineEditTable(self):
        row = self.tableWidget.currentRow()

        if row != -1:
            self.lineEdit_Fname.setText(self.Contacts[row]['Fname'])
            self.lineEdit_Lname.setText(self.Contacts[row]['Lname'])
            self.lineEdit_phone.setText(self.Contacts[row]['phone'])
            self.lineEdit_email.setText(self.Contacts[row]['email'])

    def Empty(self):
        self.lineEdit_Fname.clear()
        self.lineEdit_Lname.clear()
        self.lineEdit_phone.clear()
        self.lineEdit_email.clear()

    def WebScr(self):
        self.labelError_2.clear()
        try:
            web = "http://www.fakenamegenerator.com/"
            htmlDownload = requests.get(web, headers={'User-Agent': 'Winx64'})
            parser = etree.HTML(str(BeautifulSoup(htmlDownload.content, "html.parser")))

            name = parser.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/h3')[0].text.split()
            Fname = name[0]
            Lname = name[2]
            phone = parser.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[4]/dd/text()')[0]
            email = parser.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[9]/dd/text()')[0].replace(" ", "")


            self.lineEdit_Fname_2.setText(Fname)
            self.lineEdit_Lname_2.setText(Lname)
            self.lineEdit_phone_2.setText('+1' + phone)
            self.lineEdit_email_2.setText(email)

            self.Contacts.append({
                'Fname': Fname,
                'Lname': Lname,
                'email': email,
                'phone': phone
            })

            self.Table()
            self.Empty()

        except:
            self.labelError_2.setText("Error in connecting to internet.")

    def FindContact(self):
        text = self.textBrowser.toPlainText()

        names = "\n".join(re.findall('[@]([\w]+)', text))
        if not names: names = "Nothing Found"
        phones = "\n".join(re.findall('[#]([\d]+)', text))
        if not phones: phones = "Nothing Found"

        self.textBrowser_2.setText(names)
        self.textBrowser_3.setText(phones)

    def Open(self):
        try:
            with open("DB.txt", "r") as f:
                self.Contacts = json.loads(f.read())

        except:
            with open("DB.txt", "w") as f:
                pass

    def Save(self):
        if self.horizontalSlider_2.value() == 1:
            with open("DB.txt", "w") as f:
                f.write(json.dumps(self.Contacts))

            self.labelError.setText("Saved to DB.txt")
            self.labelError_2.setText("Saved to DB.txt")

            QtWidgets.QApplication.processEvents()
            sleep(1)
            self.horizontalSlider_2.setValue(0)


if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()

    ui = Gui()
    ui.setupUi(Main)
    ui.Open()
    ui.Table()
    ui.pushButton_first.clicked.connect(lambda x: ui.Table("Fname"))
    ui.pushButton_last.clicked.connect(lambda x: ui.Table("Lname"))
    ui.horizontalSlider.valueChanged.connect(ui.Theme)
    ui.horizontalSlider_2.valueChanged.connect(ui.Save)
    ui.pushButton_add.clicked.connect(ui.AddContacts)
    ui.pushButton_update.clicked.connect(ui.UpdateContacts)
    ui.pushButton_remove.clicked.connect(ui.RemoveContacts)
    ui.pushButton_add_2.clicked.connect(ui.WebScr)
    ui.pushButton_Find.clicked.connect(ui.FindContact)
    ui.tabWidget.currentChanged.connect(ui.Tabs)
    ui.tableWidget.itemSelectionChanged.connect(ui.LineEditTable)

    Main.show()
    sys.exit(APP.exec_())