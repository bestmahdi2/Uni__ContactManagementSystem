import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from Program import Ui_MainWin
from PyQt5 import QtCore, QtGui, QtWidgets
from os import getcwd, path

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Gui(Ui_MainWin):
    def __init__(self):
        self.ContactsList = []
        self.ReadTXT()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.SelectUpdate()
        self.lineEdit_path.setText(getcwd())
        self.lineEdit_error.setVisible(False)

        self.actionOpen_Database.triggered.connect(lambda x: self.acts('open'))
        self.actionSave_Database.triggered.connect(lambda x: self.acts('save'))

        self.actionManual.triggered.connect(lambda x: self.acts('manual'))
        self.actionFrom_Web.triggered.connect(lambda x: self.acts('web'))
        self.actionRemove.triggered.connect(lambda x: self.acts('remove'))
        self.actionChange.triggered.connect(lambda x: self.acts('change'))
        self.actionDelete_All.triggered.connect(lambda x: self.acts('deleteAll'))
        self.actionContacts_List.triggered.connect(lambda x: self.acts('list'))
        self.actionIdentify.triggered.connect(lambda x: self.acts('identify'))

        self.actionBy_Name.triggered.connect(lambda x: self.acts('searchf'))
        self.actionBy_Last_Name.triggered.connect(lambda x: self.acts('searchl'))
        self.actionBy_Email_Address.triggered.connect(lambda x: self.acts('searche'))
        self.actionBy_Phone_Number.triggered.connect(lambda x: self.acts('searchp'))

        self.actionFirst_Name.triggered.connect(lambda x: self.acts('sortf'))
        self.actionFirst_Name.triggered.connect(lambda x: self.acts('sortl'))

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def acts(self, act):
        if act == 'open':
            self.ReadTXT()
            self.SelectUpdate()
            self.EmptyLineEdits1()

        elif act == 'save':
            self.tabWidget.setCurrentIndex(5)

        elif act == "manual" or act == "remove" or act == "change":
            self.tabWidget.setCurrentIndex(0)
            self.comboBox_select.setCurrentIndex(-1)
            self.EmptyLineEdits1()

        elif act == "web":
            self.tabWidget.setCurrentIndex(3)

        elif act == "deleteAll":
            self.ContactsList = []
            self.SelectUpdate()
            self.EmptyLineEdits1()
            self.EmptyLineEdits2()
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("All Contacts were deleted successfully")

        elif act == "list":
            self.tabWidget.setCurrentIndex(1)

        elif act == "identify":
            self.tabWidget.setCurrentIndex(4)

        elif act == "searchf":
            self.tabWidget.setCurrentIndex(2)
            self.comboBox_search.setCurrentIndex(0)

        elif act == "searchl":
            self.tabWidget.setCurrentIndex(2)
            self.comboBox_search.setCurrentIndex(1)

        elif act == "searche":
            self.tabWidget.setCurrentIndex(2)
            self.comboBox_search.setCurrentIndex(2)

        elif act == "searchp":
            self.tabWidget.setCurrentIndex(2)
            self.comboBox_search.setCurrentIndex(3)

        elif act == "sortf":
            self.tabWidget.setCurrentIndex(1)
            self.pushButton_sort_name.click()

        elif act == "sortl":
            self.tabWidget.setCurrentIndex(1)
            self.pushButton_sort_name2.click()

    def ClickContactsAdd(self):
        self.lineEdit_error.setVisible(False)

        continuee = True
        name = self.lineEdit_name.text()
        name2 = self.lineEdit_name2.text()
        email = self.lineEdit_email.text()
        tele = self.lineEdit_telephone.text()

        if name == "":
            continuee = False
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Name Box Is Empty")
        elif email == "":
            pass
        elif self.VarifyEmail(email) == False:
            continuee = False
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Email Is Not Valid")

        if continuee == True:
            self.ContactsList.append({
                'name': name,
                'name2': name2,
                'email': email,
                'tele': tele
            })

            self.SelectUpdate()
            self.EmptyLineEdits1()

    def ClickContactsRemove(self):
        self.lineEdit_error.setVisible(False)
        contactIndex = self.comboBox_select.currentIndex()

        if contactIndex == -1:
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Select A Contact First")
        else:
            self.ContactsList.pop(contactIndex)
            self.SelectUpdate()
            self.EmptyLineEdits1()

    def ClickContactsChange(self):
        self.lineEdit_error.setVisible(False)
        contactIndex = self.comboBox_select.currentIndex()

        if contactIndex == -1:
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Select A Contact First")
        else:
            continuee = True
            name = self.lineEdit_name.text()
            name2 = self.lineEdit_name2.text()
            email = self.lineEdit_email.text()
            tele = self.lineEdit_telephone.text()

            if name == "":
                continuee = False
                self.lineEdit_error.setVisible(True)
                self.lineEdit_error.setText("Name Box Is Empty")
            elif email == "":
                pass
            elif self.VarifyEmail(email) == False:
                continuee = False
                self.lineEdit_error.setVisible(True)
                self.lineEdit_error.setText("Email Is Not Valid")

            if continuee == True:
                self.ContactsList[contactIndex] = {
                    'name': name,
                    'name2': name2,
                    'email': email,
                    'tele': tele}

                self.SelectUpdate()
                self.EmptyLineEdits1()

    def SortName(self):
        sorted_list = [i for i in sorted(self.ContactsList, key=lambda obj: obj['name'])]
        self.tableWidget_sort.setRowCount(0)

        for i in range(0, len(sorted_list)):
            self.tableWidget_sort.insertRow(i)
            self.tableWidget_sort.setItem(i, 0, QtWidgets.QTableWidgetItem(sorted_list[i]['name']))
            self.tableWidget_sort.setItem(i, 1, QtWidgets.QTableWidgetItem(sorted_list[i]['name2']))
            self.tableWidget_sort.setItem(i, 2, QtWidgets.QTableWidgetItem(sorted_list[i]['tele']))
            self.tableWidget_sort.setItem(i, 3, QtWidgets.QTableWidgetItem(sorted_list[i]['email']))

    def SortName2(self):
        sorted_list = [i for i in sorted(self.ContactsList, key=lambda obj: obj['name2'])]
        self.tableWidget_sort.setRowCount(0)

        for i in range(0, len(sorted_list)):
            self.tableWidget_sort.insertRow(i)
            self.tableWidget_sort.setItem(i, 0, QtWidgets.QTableWidgetItem(sorted_list[i]['name']))
            self.tableWidget_sort.setItem(i, 1, QtWidgets.QTableWidgetItem(sorted_list[i]['name2']))
            self.tableWidget_sort.setItem(i, 2, QtWidgets.QTableWidgetItem(sorted_list[i]['tele']))
            self.tableWidget_sort.setItem(i, 3, QtWidgets.QTableWidgetItem(sorted_list[i]['email']))

    def SelectUpdate(self):
        self.comboBox_select.clear()
        contact = [f"{i['name']}, {i['name2']}" for i in self.ContactsList]
        self.comboBox_select.addItems(contact)
        self.comboBox_select.setCurrentIndex(-1)

    def EmptyLineEdits1(self):
        self.lineEdit_name.clear()
        self.lineEdit_name2.clear()
        self.lineEdit_email.clear()
        self.lineEdit_telephone.clear()

    def EmptyLineEdits2(self):
        self.lineEdit_Wname.clear()
        self.lineEdit_Wname2.clear()
        self.lineEdit_Wemail.clear()
        self.lineEdit_Wtelephone.clear()

    def SelectContact(self):
        contactIndex = self.comboBox_select.currentIndex()

        if self.ContactsList:
            self.lineEdit_name.setText(self.ContactsList[contactIndex]['name'])
            self.lineEdit_name2.setText(self.ContactsList[contactIndex]['name2'])
            self.lineEdit_email.setText(self.ContactsList[contactIndex]['email'])
            self.lineEdit_telephone.setText(self.ContactsList[contactIndex]['tele'])

    def VarifyEmail(self, address):
        import re
        if address != "":
            pattern = r'^([0-9A-Za-z]|\.|\_|\-)+[@]([0-9A-Za-z]|\_|\-|\.)+[.][A-Za-z]{2,4}$'

            if re.search(pattern, address.replace(" ", "")):
                return True
            else:
                return False

    def Search(self):
        self.lineEdit_error.setVisible(False)

        char = self.lineEdit_search.text()

        if char == "":
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Enter Text In Search Box")
        else:
            index = self.comboBox_search.currentIndex()
            indexes = {0: 'name', 1: 'name2', 2: 'email', 3: 'tele'}

            searched = []
            for i in self.ContactsList:
                if char.lower() in i[indexes[index]].lower():
                    searched.append(i)

            row = 0
            self.tableWidget_search.setRowCount(0)
            for i in range(0, len(searched)):
                self.tableWidget_search.insertRow(row)
                self.tableWidget_search.setItem(row, 0, QtWidgets.QTableWidgetItem(searched[i]['name']))
                self.tableWidget_search.setItem(row, 1, QtWidgets.QTableWidgetItem(searched[i]['name2']))
                self.tableWidget_search.setItem(row, 2, QtWidgets.QTableWidgetItem(searched[i]['tele']))
                self.tableWidget_search.setItem(row, 3, QtWidgets.QTableWidgetItem(searched[i]['email']))

    def ReceiveWeb(self):
        from bs4 import BeautifulSoup
        from lxml import etree
        from requests import get
        from random import randint

        self.lineEdit_error.setVisible(False)

        HEADERS = ({'User-Agent': 'Application'})

        site = "https://www.random-name-generator.com/united-states?gender=&n=1&s=" + str(randint(10000, 99999))

        try:
            webpage = get(site, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")
            dom = etree.HTML(str(soup))

            name = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[1]/text()')[0].split()[0]
            name2 = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[1]/text()')[0].split()[1]
            phone = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[3]/text()')[0]
            phone = "+1" + phone.replace("(", "").replace(") ", "").replace("+1", "").split()[0].replace("-", " ").replace(".", " ").replace(" ", "")
            email = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[2]/dd[1]/text()')[0].replace("\n", "")

            self.lineEdit_Wname.setText(name)
            self.lineEdit_Wname2.setText(name2)
            self.lineEdit_Wemail.setText(email)
            self.lineEdit_Wtelephone.setText(phone)

        except:
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Website Is Not Reachable - No Internet")

    def ClickWebAdd(self):
        self.lineEdit_error.setVisible(False)

        continuee = True
        name = self.lineEdit_Wname.text()
        name2 = self.lineEdit_Wname2.text()
        email = self.lineEdit_Wemail.text()
        tele = self.lineEdit_Wtelephone.text()

        if name == "":
            continuee = False
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Name Box Is Empty")
        elif email == "":
            pass
        elif self.VarifyEmail(email) == False:
            continuee = False
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Email Is Not Valid")

        if continuee == True:
            self.ContactsList.append({
                'name': name,
                'name2': name2,
                'email': email,
                'tele': tele
            })

            self.SelectUpdate()
            self.EmptyLineEdits1()
            self.EmptyLineEdits2()

    def IdentifyTextContact(self):
        import re

        names = "\n".join(re.findall(r'[@](\w+)', self.textEdit_get.toPlainText()))
        tele = "\n".join(re.findall(r'[#]([0-9]+)', self.textEdit_get.toPlainText()))

        if names == "":
            names = "*No Name!*"

        if tele == "":
            tele = "*No Telephone!*"

        show = f'Names:\n{names}\n\nTelephones:\n{tele}'

        self.textEdit_give.setText(show)

    def Save(self):
        self.lineEdit_error.setVisible(False)
        location = self.lineEdit_path.text()

        continuee = True
        if not path.isdir(location):
            continuee = False
            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Path Is Not Valid")

        return continuee

    def SaveTXT(self):
        if self.Save():
            location = self.lineEdit_path.text()
            with open(location + "\\Contacts.txt", "w") as file:
                file.write(json.dumps(self.ContactsList))

            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Done!")

    def SaveJson(self):
        if self.Save():
            location = self.lineEdit_path.text()
            with open(location + "\\Contacts.json", "w") as file:
                json.dump(self.ContactsList, file)

            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Done!")

    def SaveXML(self):
        if self.Save() and self.ContactsList:
            location = self.lineEdit_path.text()
            with open(location + "\\Contacts.xml", "w") as file:
                parsed = parseString(dicttoxml(self.ContactsList, attr_type=False, custom_root='Person'))
                file.write(parsed.toprettyxml())

            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Done!")

    def SaveCMS(self):
        if self.Save():
            location = self.lineEdit_path.text()
            with open(location + "\\Contacts.cms", "wb") as file:
                import pickle
                pickle.dump(self.ContactsList, file)

            self.lineEdit_error.setVisible(True)
            self.lineEdit_error.setText("Done!")

    def ReadTXT(self):
        try:
            with open("Contacts.txt", "r") as file:
                self.ContactsList = json.loads(file.read())

        except:
            self.ContactsList = []
            with open("Contacts.txt", "w") as file:
                pass

if __name__ == "__main__":
    import sys
    program = QtWidgets.QApplication(sys.argv)
    Page = QtWidgets.QMainWindow()
    gui = Gui()
    gui.setupUi(Page)

    gui.pushButton_add.clicked.connect(gui.ClickContactsAdd)
    gui.pushButton_remove.clicked.connect(gui.ClickContactsRemove)
    gui.pushButton_change.clicked.connect(gui.ClickContactsChange)
    gui.pushButton_sort_name.clicked.connect(gui.SortName)
    gui.pushButton_sort_name2.clicked.connect(gui.SortName2)
    gui.pushButton_search.clicked.connect(gui.Search)
    gui.pushButton_Wrecivie.clicked.connect(gui.ReceiveWeb)
    gui.pushButton_Wadd.clicked.connect(gui.ClickWebAdd)
    gui.pushButton_identify.clicked.connect(gui.IdentifyTextContact)
    gui.pushButton_xml.clicked.connect(gui.SaveXML)
    gui.pushButton_txt.clicked.connect(gui.SaveTXT)
    gui.pushButton_json.clicked.connect(gui.SaveJson)
    gui.pushButton_cms.clicked.connect(gui.SaveCMS)
    gui.comboBox_select.currentIndexChanged.connect(gui.SelectContact)

    Page.show()
    sys.exit(program.exec_())
