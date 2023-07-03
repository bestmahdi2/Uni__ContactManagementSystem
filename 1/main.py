import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import requests
from bs4 import BeautifulSoup
from MainPage import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
import sys
import re

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class ContactsManager(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def Defaults(self):
        self.Database = []
        self.loadToProgram()
        self.ToDo = ""

        self.label_select.setVisible(False)
        self.label_change.setVisible(False)
        self.label_first.setVisible(False)
        self.label_last.setVisible(False)
        self.label_email.setVisible(False)
        self.label_phone.setVisible(False)
        self.lineEdit_first.setVisible(False)
        self.lineEdit_last.setVisible(False)
        self.lineEdit_email.setVisible(False)
        self.lineEdit_phone.setVisible(False)
        self.comboBox_select.setVisible(False)
        self.pushButton_apply.setVisible(False)
        self.pushButton_save.setVisible(False)
        self.label_error1.setVisible(False)
        self.label_error2.setVisible(False)
        self.label_error3.setVisible(False)

        self.DatabaseToCombo()
        self.comboBox_select.setCurrentIndex(-1)
        self.DatabaseToTable()

    def BtnMainAdd(self):
        self.label_error1.setVisible(False)
        self.label_select.setVisible(False)
        self.comboBox_select.setVisible(False)
        self.label_change.setVisible(True)
        self.label_first.setVisible(True)
        self.label_last.setVisible(True)
        self.label_email.setVisible(True)
        self.label_phone.setVisible(True)
        self.lineEdit_first.setVisible(True)
        self.lineEdit_last.setVisible(True)
        self.lineEdit_email.setVisible(True)
        self.lineEdit_phone.setVisible(True)
        self.pushButton_apply.setVisible(True)
        self.pushButton_save.setVisible(True)

        self.ToDo = "add"
        self.comboBox_select.setCurrentIndex(-1)
        self.EmptyLineEdits1()

    def BtnMainRemove(self):
        self.label_error1.setVisible(False)
        self.label_first.setVisible(False)
        self.label_last.setVisible(False)
        self.label_email.setVisible(False)
        self.label_phone.setVisible(False)
        self.lineEdit_first.setVisible(False)
        self.lineEdit_last.setVisible(False)
        self.lineEdit_email.setVisible(False)
        self.lineEdit_phone.setVisible(False)
        self.label_select.setVisible(True)
        self.comboBox_select.setVisible(True)
        self.label_change.setVisible(True)
        self.pushButton_apply.setVisible(True)
        self.pushButton_save.setVisible(True)

        self.ToDo = "remove"
        self.comboBox_select.setCurrentIndex(-1)
        self.EmptyLineEdits1()

    def BtnMainUpdate(self):
        self.label_error1.setVisible(False)
        self.label_select.setVisible(True)
        self.label_change.setVisible(True)
        self.label_first.setVisible(True)
        self.label_last.setVisible(True)
        self.label_email.setVisible(True)
        self.label_phone.setVisible(True)
        self.lineEdit_first.setVisible(True)
        self.lineEdit_last.setVisible(True)
        self.lineEdit_email.setVisible(True)
        self.lineEdit_phone.setVisible(True)
        self.comboBox_select.setVisible(True)
        self.pushButton_apply.setVisible(True)
        self.pushButton_save.setVisible(True)

        self.ToDo = "update"
        self.comboBox_select.setCurrentIndex(-1)
        self.EmptyLineEdits1()

    def BtnApply(self):
        if self.ToDo == "add":
            self.label_error1.setVisible(False)
            fname = self.lineEdit_first.text()
            lname = self.lineEdit_last.text()
            email = self.lineEdit_email.text()
            phone = self.lineEdit_phone.text()

            if fname != '':
                if self.EmailVarify(email) == True:
                    self.Database.append({
                        "first name": fname,
                        "last name": lname,
                        "email": email,
                        "phone": phone
                    })
                    self.DatabaseToCombo()
                    self.DatabaseToTable()
                    self.EmptyLineEdits1()
                else:
                    self.label_error1.setVisible(True)
                    self.label_error1.setText("Email Address is invalid")

            else:
                self.label_error1.setVisible(True)
                self.label_error1.setText("Enter a name at least")

        elif self.ToDo == "remove":
            toDelete = self.comboBox_select.currentIndex()
            if toDelete == -1:
                self.label_error1.setVisible(True)
                self.label_error1.setText("No contact selected")

            else:
                self.label_error1.setVisible(False)
                self.Database.pop(toDelete)
                self.DatabaseToCombo()
                self.DatabaseToTable()
                self.EmptyLineEdits1()

        else:
            toUpdate = self.comboBox_select.currentIndex()
            if toUpdate == -1:
                self.label_error1.setVisible(True)
                self.label_error1.setText("No contact selected")

            else:
                self.label_error1.setVisible(False)

                fname = self.lineEdit_first.text()
                lname = self.lineEdit_last.text()
                email = self.lineEdit_email.text()
                phone = self.lineEdit_phone.text()

                if fname != '':
                    if self.EmailVarify(email) == True:
                        self.Database[toUpdate] = {
                            "first name": fname,
                            "last name": lname,
                            "email": email,
                            "phone": phone
                        }

                        self.DatabaseToCombo()
                        self.DatabaseToTable()
                        self.comboBox_select.setCurrentIndex(-1)
                        self.EmptyLineEdits1()

                    else:
                        self.label_error1.setVisible(True)
                        self.label_error1.setText("Email Address is invalid")
                else:
                    self.label_error1.setVisible(True)
                    self.label_error1.setText("Enter a name at least")

    def BtnSortFirstName(self):
        self.SortContact("first name")

    def BtnSortLastName(self):
        self.SortContact("last name")

    def BtnExtract(self):
        self.textEdit_output1.clear()
        self.textEdit_output2.clear()

        text = self.textEdit_input.toPlainText()
        if text != "":
            self.label_error2.setVisible(False)

            name, phone = self.ContactExtract(text)

            final_name = '\n'.join(map(str, name))
            final_phone = '\n'.join(map(str, phone))

            if final_name:
                self.textEdit_output1.setText(final_name)
            else:
                self.textEdit_output1.setText("No contact name were found !")

            if final_phone:
                self.textEdit_output2.setText(final_phone)
            else:
                self.textEdit_output2.setText("No number were found !")

        else:
            self.label_error2.setVisible(True)
            self.label_error2.setText("Input is empty")

    def DatabaseToCombo(self):
        self.comboBox_select.clear()
        if len(self.Database) > 0:
            tempList = []

            for i in self.Database:
                tempList.append(i['first name'] + " " + i['last name'])

            self.comboBox_select.addItems(tempList)

    def EmptyLineEdits1(self):
        self.lineEdit_first.clear()
        self.lineEdit_last.clear()
        self.lineEdit_email.clear()
        self.lineEdit_phone.clear()

    def EmptyLineEdits2(self):
        self.lineEdit_first_2.clear()
        self.lineEdit_last_2.clear()
        self.lineEdit_email_2.clear()
        self.lineEdit_phone_2.clear()

    def ComboEditLine(self):
        toEditLine = self.comboBox_select.currentIndex()

        if self.ToDo == "update":
            self.lineEdit_first.setText(self.Database[toEditLine]["first name"])
            self.lineEdit_last.setText(self.Database[toEditLine]["last name"])
            self.lineEdit_email.setText(self.Database[toEditLine]["email"])
            self.lineEdit_phone.setText(self.Database[toEditLine]["phone"])

    def DatabaseToTable(self, database=[]):
        if database == []:
            database = self.Database

        self.tableWidget.setRowCount(0)
        for i in range(len(database)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(database[i]['first name']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(database[i]['last name']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(database[i]['phone']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(database[i]['email']))

    def ContactExtract(self, text):
        names = re.findall(r'[@]([\w]+)', text)
        phones = re.findall(r'[#]([\d]+)', text)

        return names, phones

    def EmailVarify(self, email):
        tempList = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$)", email)

        if email == "":
            return True
        elif tempList == []:
            return False
        else:
            return True

    def WebScrap(self):
        try:
            self.label_error3.setVisible(False)
            response = requests.get('https://www.fakenamegenerator.com/', headers={'user-agent': 'Sth here'})
            soup = BeautifulSoup(response.text, 'html.parser')

            names = [str(i).replace("<h3>", "").replace("</h3>", "") for i in soup.find_all("h3")][0].split()
            firstname = names[0] + " " + names[1]
            lastname = names[2]

            phones = [str(i).replace("<dd>", "").replace("</dd>", "") for i in soup.find_all("dd")]
            phone = "+" + phones[4] + phones[3]
            email = phones[8].split()[0]

            self.lineEdit_first_2.setText(firstname)
            self.lineEdit_last_2.setText(lastname)
            self.lineEdit_email_2.setText(email)
            self.lineEdit_phone_2.setText(phone)

        except:
            self.label_error3.setVisible(True)
            self.label_error3.setText("No connection to internet")

    def WebAdd(self):
        fname = self.lineEdit_first_2.text()
        if fname != '':
            self.label_error3.setVisible(False)
            fname = self.lineEdit_first_2.text()
            lname = self.lineEdit_last_2.text()
            email = self.lineEdit_email_2.text()
            phone = self.lineEdit_phone_2.text()

            if self.EmailVarify(email) == True:
                self.Database.append({
                    "first name": fname,
                    "last name": lname,
                    "email": email,
                    "phone": phone
                })
                self.DatabaseToCombo()
                self.DatabaseToTable()
                self.EmptyLineEdits2()
            else:
                self.label_error3.setVisible(True)
                self.label_error3.setText("Email Address is invalid")

        else:
            self.label_error3.setVisible(True)
            self.label_error3.setText("Enter a name at least")

    def SortContact(self, sort):
        tempList = [i for i in sorted(self.Database, key=lambda obj: obj[sort])]
        self.DatabaseToTable(tempList)

    def SaveToFile(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle('Save as ...')
        messageBox.setIcon(QtWidgets.QMessageBox.Question)
        messageBox.setText('What format would you like to save your file ?')
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save)

        buttonJson = messageBox.button(QtWidgets.QMessageBox.Yes)
        buttonJson.setText('Json')
        buttonXML = messageBox.button(QtWidgets.QMessageBox.No)
        buttonXML.setText('XML')
        buttonTXT = messageBox.button(QtWidgets.QMessageBox.Save)
        buttonTXT.setText('TXT')

        messageBox.exec_()

        if messageBox.clickedButton() == buttonJson:
            file = open('database.json', 'w')
            json.dump(self.Database, file)
            file.close()

        elif messageBox.clickedButton() == buttonXML:
            dom = parseString(dicttoxml(self.Database, attr_type=False))
            file = open("database.xml", 'w')
            makePrrety = dom.toprettyxml()
            file.write(makePrrety)
            file.close()

        else:
            file = open('database.txt', 'w')
            file.write(json.dumps(self.Database))
            file.close()

    def loadToProgram(self):
        try:
            file = open("database.txt", 'r')
            self.Database = json.loads(file.read())
            file.close()

        except:
            file = open("database.txt", 'w')
            file.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    MainWindow = QtWidgets.QMainWindow()

    ui = ContactsManager()
    ui.setupUi(MainWindow)
    ui.Defaults()

    ui.pushButton_MainAdd.clicked.connect(ui.BtnMainAdd)
    ui.pushButton_MainRemove.clicked.connect(ui.BtnMainRemove)
    ui.pushButton_MainUpdate.clicked.connect(ui.BtnMainUpdate)
    ui.pushButton_apply.clicked.connect(ui.BtnApply)
    ui.pushButton_save.clicked.connect(ui.SaveToFile)
    ui.comboBox_select.currentIndexChanged.connect(ui.ComboEditLine)
    ui.pushButton_firstname.clicked.connect(ui.BtnSortFirstName)
    ui.pushButton_lastname.clicked.connect(ui.BtnSortLastName)
    ui.pushButton_extract.clicked.connect(ui.BtnExtract)
    ui.pushButton_get.clicked.connect(ui.WebScrap)
    ui.pushButton_add.clicked.connect(ui.WebAdd)

    MainWindow.show()
    sys.exit(app.exec_())
