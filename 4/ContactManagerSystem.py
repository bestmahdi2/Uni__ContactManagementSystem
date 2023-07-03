import requests
from PyQt5 import QtCore, QtWidgets
import sys
import re
import json
from bs4 import BeautifulSoup
from Files.Window import Ui_MainWindow as WINDOW
from Files.Text import Ui_Dialog as TEXT
from Files.Add import Ui_Dialog as ADD
from Files.Scraping import Ui_Dialog as SCRAP
from Files.Edit_List import Ui_Dialog as EDITLIST

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GUI(WINDOW):
    def setupUi(self, WINDOW):
        super().setupUi(WINDOW)

    def retranslateUi(self, WINDOW):
        super().retranslateUi(WINDOW)

    def listMaker(self):
        self.MainList = []

    def dialogEditList(self):
        QDialog = QtWidgets.QDialog()
        self.EL = EDITLIST()
        self.EL.setupUi(QDialog)

        self.tableUpdate()
        self.EL.pushButtonAdd.clicked.connect(self.dialogAdd)
        self.EL.pushButtonRemove.clicked.connect(self.deleteCon)
        self.EL.pushButtonEdit.clicked.connect(self.editCon)
        self.EL.pushButtonFName.clicked.connect(self.SortFName)
        self.EL.pushButton_LName.clicked.connect(self.SortLName)

        QDialog.show()
        QDialog.exec_()

    def dialogAdd(self):
        QDialog = QtWidgets.QDialog()
        self.Add = ADD()
        self.Add.setupUi(QDialog)

        self.Add.pushButton_Add.clicked.connect(lambda x: self.addCon(self.Add))

        QDialog.show()
        QDialog.exec_()

    def dialogScrap(self):
        QDialog = QtWidgets.QDialog()
        self.Scr = SCRAP()
        self.Scr.setupUi(QDialog)

        self.Scr.pushButton_Web.clicked.connect(self.webScraping)
        self.Scr.pushButton_Add.clicked.connect(lambda x: self.addCon(self.Scr))

        QDialog.show()
        QDialog.exec_()

    def dialogText(self):
        QDialog = QtWidgets.QDialog()
        self.Text = TEXT()
        self.Text.setupUi(QDialog)

        self.Text.pushButton_Identify.clicked.connect(self.identifyCon)

        QDialog.show()
        QDialog.exec_()

    def addCon(self, cls):
        cls.labelError.clear()
        fName = cls.lineEdit.text()
        lName = cls.lineEdit_2.text()
        email = cls.lineEdit_3.text()
        phone = cls.lineEdit_4.text()

        help = True

        if fName == "":
            help = False
            cls.labelError.setText("Empty Name!")

        elif self.EmailCheck(email) != True:
            help = False
            cls.labelError.setText("Invalid Email!")

        if help:
            contact = {"fname": fName, "lname": lName, "email": email, "phone": phone}

            if contact not in self.MainList:
                self.MainList.append(contact)

            cls.lineEdit.clear()
            cls.lineEdit_2.clear()
            cls.lineEdit_3.clear()
            cls.lineEdit_4.clear()
            cls.labelError.clear()

            try:
                self.tableUpdate()
            except:
                pass

    def deleteCon(self):
        self.EL.labelError.clear()
        contact = self.EL.tableWidgetListEdit.currentRow()

        if contact != -1:
            self.MainList.pop(contact)
            self.tableUpdate()
        else:
            self.EL.labelError.setText("No Contact Selected !")

    def editCon(self):
        self.EL.labelError.clear()

        rows = self.EL.tableWidgetListEdit.rowCount()
        contacts = []
        for i in range(rows):
            contact = {"fname": self.EL.tableWidgetListEdit.item(i, 0).text(), "lname": self.EL.tableWidgetListEdit.item(i, 1).text(),
                    "email": self.EL.tableWidgetListEdit.item(i, 2).text(), "phone": self.EL.tableWidgetListEdit.item(i, 3).text()}

        if contacts == self.MainList:
            self.EL.labelError.setText("Nothing Changed !")

        else:
            self.EL.labelError.setText("Changes Saved To Program !")
            self.MainList = contacts

    def SortFName(self):
        self.MainList = [i for i in sorted(self.MainList, key=lambda j: j["fname"])]
        self.tableUpdate()

    def SortLName(self):
        self.MainList = [i for i in sorted(self.MainList, key=lambda j: j["lname"])]
        self.tableUpdate()

    def EmailCheck(self, email):
        reg = '^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.][A-Za-z]{2,3}$'

        if re.search(reg, email.lower()) or email == "":
            return True
        else:
            return False

    def identifyCon(self):
        input = self.Text.textEdit.toPlainText()

        allNumber = re.findall('[#][0-9]+', input)
        allName = re.findall('[@][A-Za-z]+', input)

        numbers = ""
        for i in allNumber:
            numbers = numbers + i.replace("#", "") + "\n"

        name = ""
        for i in allName:
            name = name + i.replace("@", "") + "\n"

        self.Text.textEdit_2.setText("Phones:\n" + numbers + "\nNames:\n" + name)

    def clickOpen(self):
        try:
            self.labelError.clear()
            with open('TxtDatabase.txt', 'r') as file:
                self.MainList = json.loads(file.read())
                self.labelError.setText("Opened Database successfully.")

                try:
                    self.tableUpdate()
                except:
                    pass

        except:
            self.labelError.setText("No Database were found, a new one created.")
            self.clickSave("no")

    def clickSave(self, clear="yes"):
        try:
            if clear == "yes":
                self.labelError.clear()

            with open('TxtDatabase.txt', 'w') as file:
                json.dump(self.MainList, file)
                self.labelError.setText("Saved Database successfully.")
        except:
            self.labelError.setText("Can't Save txt file, it might be open by other program.")

    def tableUpdate(self):
        self.EL.tableWidgetListEdit.setRowCount(0)

        for i in range(len(self.MainList)):
            self.EL.tableWidgetListEdit.insertRow(i)
            info = self.MainList[i]
            self.EL.tableWidgetListEdit.setItem(i, 0, QtWidgets.QTableWidgetItem(info['fname']))
            self.EL.tableWidgetListEdit.setItem(i, 1, QtWidgets.QTableWidgetItem(info['lname']))
            self.EL.tableWidgetListEdit.setItem(i, 2, QtWidgets.QTableWidgetItem(info['phone']))
            self.EL.tableWidgetListEdit.setItem(i, 3, QtWidgets.QTableWidgetItem(info['email']))

    def webScraping(self):
        try:
            self.Scr.labelError.clear()
            response = requests.get('https://www.fakenamegenerator.com', headers={'user-agent': 'CMS'})
            soup = BeautifulSoup(response.text, 'html.parser')
            fname, _, lname = str(soup.find_all("h3")[0]).replace("<h3>", "").replace("</h3>", "").split()
            phone = "+1" + str(soup.find_all("dd")[3]).replace("<dd>", "").replace("</dd>", "")
            email = str(soup.find_all("dd")[8]).replace("<dd>", "").split()[0]

            self.Scr.lineEdit.setText(fname)
            self.Scr.lineEdit_2.setText(lname)
            self.Scr.lineEdit_3.setText(email)
            self.Scr.lineEdit_4.setText(phone)

        except:
            self.Scr.labelError.setText("Problem In Internet Connection !")


if __name__ == '__main__':
    QApplication = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()

    obj = GUI()
    obj.setupUi(QMainWindow)

    obj.listMaker()
    obj.clickOpen()

    obj.pushButtonEditList.clicked.connect(obj.dialogEditList)
    obj.pushButtonIdentufy.clicked.connect(obj.dialogText)
    obj.pushButtonWeb.clicked.connect(obj.dialogScrap)
    obj.pushButtonOpen.clicked.connect(obj.clickOpen)
    obj.pushButtonSave.clicked.connect(obj.clickSave)

    QMainWindow.show()
    sys.exit(QApplication.exec_())





