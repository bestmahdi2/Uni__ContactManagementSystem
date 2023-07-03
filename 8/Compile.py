import sys
from PyQt5 import QtWidgets, QtCore
from MainWindow import Ui_MainWindow
import re
import json
from parsel import Selector
import requests


# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Contacts(Ui_MainWindow):
    def __init__(self):
        self.List = []

    def retranslateUi(self, MenuWindow):
        super().retranslateUi(MenuWindow)

    def setupUi(self, MenuWindow):
        super().setupUi(MenuWindow)

    def sortTable(self):
        if self.radioButton.isChecked():
            sortedList = [i for i in sorted(self.List, key=lambda item: item['first_name'])]
        else:
            sortedList = [i for i in sorted(self.List, key=lambda item: item['last_name'])]

        self.tableWidget.setRowCount(0)
        for i in range(0, len(sortedList)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(sortedList[i]['first_name']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(sortedList[i]['last_name']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(sortedList[i]['phone_number']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(sortedList[i]['email_address']))

    def add(self):
        self.label_error.setText("")

        get = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text()]
        dict = {"first_name": get[0], "last_name": get[1], "phone_number": get[2], "email_address": get[3]}

        if not get[0] == "":
            if self.email(get[3]):
                if dict not in self.List:
                    self.List.append(dict)
                    self.clear_update()
            else:
                self.label_error.setText("Enter a valid email address.")
        else:
            self.label_error.setText("Enter a name.")

    def edit(self):
        self.label_error.setText("")

        selectedContact = self.comboBox.currentIndex()
        if selectedContact != -1:
            get = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text()]
            dict = {"first_name": get[0], "last_name": get[1], "phone_number": get[2], "email_address": get[3]}

            if not get[0] == "":
                if self.email(get[3]):
                    if dict not in self.List:
                        self.List[selectedContact] = dict
                        self.clear_update()
                else:
                    self.label_error.setText("Enter a valid email address.")
            else:
                self.label_error.setText("Enter a name.")

        else:
            self.label_error.setText("Select a contact.")

    def remove(self):
        self.label_error.setText("")

        selectedContact = self.comboBox.currentIndex()
        if selectedContact != -1:
            self.List.pop(selectedContact)
            self.clear_update()
        else:
            self.label_error.setText("Select a contact.")

    def clear_update(self):
        # update
        self.comboBox.clear()
        self.comboBox.addItems([f"{i['first_name']} {i['last_name']}" for i in self.List])
        self.comboBox.setCurrentIndex(-1)

        # clear
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.label_error.setText("")

    def email(self, email):
        if email != "":
            pattern = '^([0-9A-Za-z]|\.|\_|\-)+[@]([0-9A-Za-z]|\_|\-|\.)+[.][A-Za-z]{2,3}$'
            if re.search(pattern, email):
                return True
            else:
                return False
        else:
            return True

    def save(self):
        file = open("contactList.txt", "w")
        file.write(json.dumps(self.List))
        file.close()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle('Success !')
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText('Program database saved in txt file !')
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)

        message.exec_()

    def open(self):
        try:
            file = open("contactList.txt", "r")
            self.List = json.loads(file.read())
            file.close()

        except:
            self.List = []
            file = open("contactList.txt", "w")
            file.close()

    def autoSelectLineEdit(self):
        if self.comboBox.currentIndex() != -1:
            self.lineEdit.setText(self.List[self.comboBox.currentIndex()]['first_name'])
            self.lineEdit_2.setText(self.List[self.comboBox.currentIndex()]['last_name'])
            self.lineEdit_3.setText(self.List[self.comboBox.currentIndex()]['phone_number'])
            self.lineEdit_4.setText(self.List[self.comboBox.currentIndex()]['email_address'])

    def web(self):
        self.label_error_2.setText("Wait ...")
        QtWidgets.QApplication.processEvents()
        website, headers = "https://www.fakenamegenerator.com/", ({'user-agent': 'Contacts Manager'})

        text = requests.get(website, headers=headers).text
        selector = Selector(text=text, type='xml')

        name = selector.css('#details > div.content > div.info > div > div.address > h3').extract_first().replace("</h3>", "").replace("<h3>", "").split()
        phone_number = "+1" + selector.css('#details > div.content > div.info > div > div.extra > dl:nth-child(5) > dd').extract_first().replace("<dd>", "").replace("</dd>", "")
        email_address = selector.css('#details > div.content > div.info > div > div.extra > dl:nth-child(12) > dd').extract_first().split()[0].replace("<dd>", "")

        first_name = name[0] + " " + name[1]
        last_name = name[2]

        self.lineEdit_6.setText(first_name)
        self.lineEdit_7.setText(last_name)
        self.lineEdit_8.setText(phone_number)
        self.lineEdit_9.setText(email_address)
        self.label_error_2.setText("")

    def clear_updateWeb(self):
        # update
        self.comboBox.clear()
        self.comboBox.addItems([f"{i['first_name']} {i['last_name']}" for i in self.List])
        self.comboBox.setCurrentIndex(-1)

        # clear
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.label_error.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.label_error_2.setText("")

    def addWeb(self):
        self.label_error.setText("")

        get = [self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text(), self.lineEdit_9.text()]
        dict = {"first_name": get[0], "last_name": get[1], "phone_number": get[2], "email_address": get[3]}

        if not get[0] == "":
            if dict not in self.List:
                self.List.append(dict)
                self.clear_updateWeb()

        else:
            self.label_error_2.setText("Click on \"Gather\" first !")

    def textRegex(self):
        inputText = self.textBrowser.toPlainText()

        names = "\n".join(re.findall(r'[@](\w+)', inputText))
        phones = "\n".join(re.findall(r'[#]([0-9]+)', inputText))

        name = "# Names found #\n" + names if names else "# No names were found ! #"
        phone = "# Phone numbers found #\n" + phones if phones else "# No phone numbers were found ! #"

        self.textBrowser_2.setText("{}\n\n{}".format(name, phone))

if __name__ == "__main__":
    Original_app = QtWidgets.QApplication(sys.argv)
    Original_window = QtWidgets.QMainWindow()

    Con = Contacts()
    Con.setupUi(Original_window)
    Con.open()
    Con.sortTable()
    Con.clear_update()

    Con.radioButton.clicked.connect(Con.sortTable)
    Con.radioButton_2.clicked.connect(Con.sortTable)
    Con.pushButton_refresh.clicked.connect(Con.sortTable)
    Con.pushButton.clicked.connect(Con.add)
    Con.pushButton_2.clicked.connect(Con.edit)
    Con.pushButton_3.clicked.connect(Con.remove)
    Con.pushButton_4.clicked.connect(Con.save)
    Con.comboBox.currentIndexChanged.connect(Con.autoSelectLineEdit)
    Con.pushButtonGather.clicked.connect(Con.web)
    Con.pushButtonAdd.clicked.connect(Con.addWeb)
    Con.pushButton_Find.clicked.connect(Con.textRegex)

    Original_window.show()
    sys.exit(Original_app.exec_())