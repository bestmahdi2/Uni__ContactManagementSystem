import json
from bs4 import BeautifulSoup
import requests
import re
from PyQt5 import QtCore, QtWidgets
from UI.Main import Ui_MainWindow
from UI.Extract import Ui_DialogEx
from UI.Manager import Ui_DialogMa
from UI.Online import Ui_DialogOn
from UI.Table import Ui_DialogTa
import sys

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Cms(Ui_MainWindow):
    def __init__(self):
        self.AllContacts = []

    def setupUi(self, MenuWindow):
        super().setupUi(MenuWindow)

        self.ReadDatabase()
        self.pushButton.clicked.connect(self.PageMa)
        self.pushButton_2.clicked.connect(self.PageTa)
        self.pushButton_3.clicked.connect(self.PageEx)
        self.pushButton_4.clicked.connect(self.PageOn)

    def retranslateUi(self, MenuWindow):
        super().retranslateUi(MenuWindow)

    ##
    def PageEx(self):
        appEx = QtWidgets.QDialog()
        self.Ex = Ui_DialogEx()
        self.Ex.setupUi(appEx)

        self.Ex.pushButton.clicked.connect(self.ExtractText)

        appEx.show()
        appEx.exec_()

    def ExtractText(self):
        name = re.findall(r'[@]([\w]+)', self.Ex.textBrowser.toPlainText())
        number = re.findall(r'[#]([\d]+)', self.Ex.textBrowser.toPlainText())

        self.Ex.textBrowser_2.setText("\n".join(name))
        self.Ex.textBrowser_3.setText("\n".join(number))

    ##
    def PageMa(self):
        appMa = QtWidgets.QDialog()
        self.Ma = Ui_DialogMa()
        self.Ma.setupUi(appMa)

        self.ComboboxMa()
        self.Ma.pushButton.clicked.connect(self.AddContact)
        self.Ma.pushButton_2.clicked.connect(self.DeleteContact)
        self.Ma.pushButton_3.clicked.connect(self.UpdateContact)
        self.Ma.comboBox.currentIndexChanged.connect(self.LineEditsComboboxMa)

        appMa.show()
        appMa.exec_()

    def AddContact(self):
        List = [self.Ma.lineEdit_name.text(), self.Ma.lineEdit_lastname.text(),
                self.Ma.lineEdit_number.text(), self.Ma.lineEdit_email.text()]

        self.Ma.label_error.clear()
        if List[0]:
            if self.Email(List[3]):
                if List not in self.AllContacts: self.AllContacts.append(List)
                try:
                    self.TableFill()
                except:
                    pass
                self.ComboboxMa()
                self.LineEditsMa([])

            else:
                self.Ma.label_error.setText("Email address is not a valid one.")

        else:
            self.Ma.label_error.setText("Name is necessary.")

    def UpdateContact(self):
        contact_index = self.Ma.comboBox.currentIndex()
        self.Ma.label_error.clear()

        if contact_index >= 0:
            List = [self.Ma.lineEdit_name.text(), self.Ma.lineEdit_lastname.text(),
                    self.Ma.lineEdit_number.text(), self.Ma.lineEdit_email.text()]

            if List[0]:
                if self.Email(List[3]):
                    self.AllContacts[contact_index] = List
                    try:
                        self.TableFill()
                    except:
                        pass
                    self.ComboboxMa()
                    self.LineEditsMa([])

                else:
                    self.Ma.label_error.setText("Email address is not a valid one.")

            else:
                self.Ma.label_error.setText("Name is necessary.")

        else:
            self.Ma.label_error.setText("No contact selected from combobox.")

    def DeleteContact(self):
        contact_index = self.Ma.comboBox.currentIndex()

        if contact_index >= 0:
            self.AllContacts.pop(contact_index)
            try:
                self.TableFill()
            except:
                pass
            self.ComboboxMa()
            self.LineEditsMa([])

        else:
            self.Ma.label_error.setText("No contact selected from combobox.")

    def Email(self, address):
        if address == "":
            return True
        else:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9]+[.][a-z0-9]{2,3}$'

            if re.search(regex, address.lower()):
                return True
            else:
                return False

    def LineEditsMa(self, List):
        if List:
            self.Ma.lineEdit_name.setText(List[0])
            self.Ma.lineEdit_lastname.setText(List[1])
            self.Ma.lineEdit_number.setText(List[2])
            self.Ma.lineEdit_email.setText(List[3])

        else:
            self.Ma.lineEdit_name.clear()
            self.Ma.lineEdit_lastname.clear()
            self.Ma.lineEdit_number.clear()
            self.Ma.lineEdit_email.clear()

    def ComboboxMa(self):
        self.Ma.comboBox.clear()
        self.Ma.comboBox.addItems(['{} {}'.format(i[0], i[1]) for i in self.AllContacts])
        self.Ma.comboBox.setCurrentIndex(-1)

    def LineEditsComboboxMa(self):
        index = self.Ma.comboBox.currentIndex()

        if index > -1:
            self.Ma.lineEdit_name.setText(self.AllContacts[index][0])
            self.Ma.lineEdit_lastname.setText(self.AllContacts[index][1])
            self.Ma.lineEdit_number.setText(self.AllContacts[index][2])
            self.Ma.lineEdit_email.setText(self.AllContacts[index][3])


    ##
    def PageOn(self):
        appOn = QtWidgets.QDialog()
        self.On = Ui_DialogOn()
        self.On.setupUi(appOn)

        self.On.pushButton.clicked.connect(self.ConnectToWeb)
        self.On.comboBox.currentIndexChanged.connect(self.LineEditsComboboxOn)
        self.On.pushButton_2.clicked.connect(self.EditWeb)

        appOn.show()
        appOn.exec_()

    def ConnectToWeb(self):
        link = "https://www.fakenamegenerator.com/"
        self.On.label_error.clear()
        self.LineEditsOn([])
        QtWidgets.QApplication.processEvents()

        try:
            html = requests.get(link, headers=({'User-Agent': 'Chrome x64'}))
            soup = BeautifulSoup(html.content, "html.parser")

            name = [i.get_text() for i in soup.select("div.address")]
            info = [i.get_text() for i in soup.select("dl.dl-horizontal")]

            List = [name[0].split()[0], name[0].split()[2],
                    "+1" + info[3].split()[1], info[8].split()[2]]

            self.LineEditsOn(List)
            self.On.label_error.setText("Added To Database.")
            self.AllContacts.append(List)
            try:
                self.TableFill()
            except:
                pass
            try:
                self.ComboboxMa()
                self.LineEditsMa([])
            except:
                pass
            self.On.comboBox.setCurrentIndex(0)
            self.On.lineEdit_edit.setText(List[0])

        except:
            self.On.label_error.setText("Connection interrupt.")

    def LineEditsOn(self, List):
        if List:
            self.On.label_name.setText(List[0])
            self.On.label_lastname.setText(List[1])
            self.On.label_number.setText(List[2])
            self.On.label_email.setText(List[3])
            self.On.comboBox.setCurrentIndex(0)

        else:
            self.On.label_name.clear()
            self.On.label_lastname.clear()
            self.On.label_number.clear()
            self.On.label_email.clear()

    def LineEditsComboboxOn(self):
        index = self.On.comboBox.currentIndex()

        if index == 0:
            self.On.lineEdit_edit.setText(self.On.label_name.text())

        elif index == 1:
            self.On.lineEdit_edit.setText(self.On.label_lastname.text())

        elif index == 2:
            self.On.lineEdit_edit.setText(self.On.label_number.text())

        else:
            self.On.lineEdit_edit.setText(self.On.label_email.text())

    def EditWeb(self):
        List = [self.On.label_name.text(), self.On.label_lastname.text(),
                self.On.label_number.text(), self.On.label_email.text()]

        index = self.On.comboBox.currentIndex()
        List[index] = self.On.lineEdit_edit.text()

        self.AllContacts[-1] = List
        self.LineEditsOn(List)
        try:
            self.TableFill()
        except:
            pass
        try:
            self.ComboboxMa()
            self.LineEditsMa([])
        except:
            pass

    ##
    def PageTa(self):
        appTa = QtWidgets.QDialog()
        self.Ta = Ui_DialogTa()
        self.Ta.setupUi(appTa)

        self.TableFill()
        self.Ta.checkBox.clicked.connect(self.SortName)
        self.Ta.checkBox_2.clicked.connect(self.SortLastName)

        appTa.show()
        appTa.exec_()

    def SortName(self):
        if self.Ta.checkBox.checkState() > 0:
            self.Ta.checkBox_2.setCheckState(0)
        else:
            self.Ta.checkBox_2.setCheckState(2)
        self.TableFill('sort')

    def SortLastName(self):
        if self.Ta.checkBox_2.checkState() > 0:
            self.Ta.checkBox.setCheckState(0)
        else:
            self.Ta.checkBox.setCheckState(2)
        self.TableFill('sort')

    def TableFill(self, index=None):
        SortList = self.AllContacts

        if index:
            index = 0 if self.Ta.checkBox.checkState() else 1
            SortList = [i for i in sorted(self.AllContacts, key=lambda item: item[index])]

        x = 0
        self.Ta.tableWidget.setRowCount(0)
        while x < len(self.AllContacts):
            self.Ta.tableWidget.insertRow(x)
            self.Ta.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(SortList[x][0]))
            self.Ta.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem(SortList[x][1]))
            self.Ta.tableWidget.setItem(x, 2, QtWidgets.QTableWidgetItem(SortList[x][2]))
            self.Ta.tableWidget.setItem(x, 3, QtWidgets.QTableWidgetItem(SortList[x][3]))
            x += 1

    ##
    def ReadDatabase(self):
        try:
            with open("ContactsDB.txt", 'r') as file:
                self.AllContacts = json.loads(file.read())

        except:
            with open("ContactsDB.txt", 'w') as file:
                pass

    def SaveDatabase(self, _):
        with open("ContactsDB.txt", 'w') as file:
            file.write(json.dumps(self.AllContacts))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    window = QtWidgets.QMainWindow()

    gui = Cms()
    gui.setupUi(window)
    window.closeEvent = gui.SaveDatabase

    window.show()
    sys.exit(app.exec_())
