import re
import sys
import json
import requests
from parsel import Selector
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from tkinter import filedialog, Tk
from PyQt5 import QtCore, QtWidgets
from Gui.MainWin import Ui_MainWindow
from Gui.Dialog_Edit import Ui_DialogEdit
from Gui.Dialog_Find import Ui_DialogFind
from Gui.Dialog_List import Ui_DialogList
from Gui.Dialog_Web import Ui_DialogWeb

class ConManSys(Ui_MainWindow):
    def retranslateUi(self, MenuWindow):
        super().retranslateUi(MenuWindow)

    def setupUi(self, MenuWindow):
        super().setupUi(MenuWindow)

    def firstStep(self):
        self.originalList = []
        self.edit = "add"
        self.open()

    def buttonMainEdit(self):
        DialogE = QtWidgets.QDialog()
        self.WindowE = Ui_DialogEdit()
        self.WindowE.setupUi(DialogE)

        self.WindowE.pushButtonAdd.clicked.connect(self.buttonChooseAdd)
        self.WindowE.pushButtonChange.clicked.connect(self.buttonChooseChange)
        self.WindowE.pushButtonDelete.clicked.connect(self.buttonChooseDelete)
        self.WindowE.pushButtonConfirm.clicked.connect(self.buttonConfirm)
        self.WindowE.comboBox.currentIndexChanged.connect(self.fillLineEdit)

        self.WindowE.label_3.setVisible(False)
        self.WindowE.label_4.setVisible(False)
        self.WindowE.label_5.setVisible(False)
        self.WindowE.label_6.setVisible(False)
        self.WindowE.lineEditFirst.setVisible(False)
        self.WindowE.lineEditLast.setVisible(False)
        self.WindowE.lineEditEmail.setVisible(False)
        self.WindowE.lineEditPhone.setVisible(False)
        self.WindowE.pushButtonConfirm.setVisible(False)
        self.WindowE.comboBox.setVisible(False)
        self.WindowE.label_order.setVisible(False)

        DialogE.show()
        DialogE.exec_()

    def buttonMainList(self):
        DialogL = QtWidgets.QDialog()
        self.WindowL = Ui_DialogList()
        self.WindowL.setupUi(DialogL)

        self.fillTable()
        self.WindowL.radioButtonName.clicked.connect(self.fillTable)
        self.WindowL.radioButtonFamily.clicked.connect(self.fillTable)

        DialogL.show()
        DialogL.exec_()

    def buttonMainFind(self):
        DialogF = QtWidgets.QDialog()
        self.WindowF = Ui_DialogFind()
        self.WindowF.setupUi(DialogF)

        self.WindowF.pushButtonFind.clicked.connect(self.buttonFind)

        DialogF.show()
        DialogF.exec_()

    def buttonMainWeb(self):
        DialogW = QtWidgets.QDialog()
        self.WindowW = Ui_DialogWeb()
        self.WindowW.setupUi(DialogW)

        self.WindowW.pushButtonWebGet.clicked.connect(self.buttonGetWeb)
        self.WindowW.pushButtonWebAdd.clicked.connect(self.buttonAddWeb)

        DialogW.show()
        DialogW.exec_()

    def buttonChooseAdd(self):
        self.edit = "add"

        self.WindowE.label_error.clear()
        self.WindowE.label_3.setVisible(True)
        self.WindowE.label_4.setVisible(True)
        self.WindowE.label_5.setVisible(True)
        self.WindowE.label_6.setVisible(True)
        self.WindowE.lineEditFirst.setVisible(True)
        self.WindowE.lineEditLast.setVisible(True)
        self.WindowE.lineEditEmail.setVisible(True)
        self.WindowE.lineEditPhone.setVisible(True)
        self.WindowE.pushButtonConfirm.setVisible(True)
        self.WindowE.pushButtonConfirm.setGeometry(QtCore.QRect(500, 560, 91, 51))
        self.WindowE.pushButtonConfirm.setEnabled(True)
        self.WindowE.comboBox.setVisible(False)
        self.WindowE.label_order.setVisible(True)
        self.WindowE.label_order.setText('Fill boxes below to add a contact')

    def buttonChooseChange(self):
        self.edit = "change"

        if self.originalList:
            self.fillComboEdit()
            self.WindowE.pushButtonConfirm.setEnabled(True)
            self.WindowE.label_error.clear()
        else:
            self.WindowE.pushButtonConfirm.setEnabled(False)
            self.WindowE.label_error.setText('No contact to change its info')

        self.WindowE.label_3.setVisible(True)
        self.WindowE.label_4.setVisible(True)
        self.WindowE.label_5.setVisible(True)
        self.WindowE.label_6.setVisible(True)
        self.WindowE.lineEditFirst.setVisible(True)
        self.WindowE.lineEditLast.setVisible(True)
        self.WindowE.lineEditEmail.setVisible(True)
        self.WindowE.lineEditPhone.setVisible(True)
        self.WindowE.pushButtonConfirm.setVisible(True)
        self.WindowE.pushButtonConfirm.setGeometry(QtCore.QRect(500, 560, 91, 51))
        self.WindowE.comboBox.setVisible(True)
        self.WindowE.label_order.setVisible(True)
        self.WindowE.label_order.setText('Choose a contact from box to change')

    def buttonChooseDelete(self):
        self.edit = "delete"

        if self.originalList:
            self.fillComboEdit()
            self.WindowE.pushButtonConfirm.setEnabled(True)
            self.WindowE.label_error.clear()
        else:
            self.WindowE.pushButtonConfirm.setEnabled(False)
            self.WindowE.label_error.setText('No contact to delete')

        self.WindowE.label_3.setVisible(False)
        self.WindowE.label_4.setVisible(False)
        self.WindowE.label_5.setVisible(False)
        self.WindowE.label_6.setVisible(False)
        self.WindowE.lineEditFirst.setVisible(False)
        self.WindowE.lineEditLast.setVisible(False)
        self.WindowE.lineEditEmail.setVisible(False)
        self.WindowE.lineEditPhone.setVisible(False)
        self.WindowE.pushButtonConfirm.setVisible(True)
        self.WindowE.pushButtonConfirm.setGeometry(QtCore.QRect(500, 310, 91, 51))
        self.WindowE.comboBox.setVisible(True)
        self.WindowE.label_order.setVisible(True)
        self.WindowE.label_order.setText('Choose a contact from box to delete')

    def buttonConfirm(self):
        if self.edit == "add":
            if self.WindowE.lineEditFirst.text():
                if self.email(self.WindowE.lineEditEmail.text()):
                    self.WindowE.label_error.clear()
                    self.originalList.append([
                        self.WindowE.lineEditFirst.text(),
                        self.WindowE.lineEditLast.text(),
                        self.WindowE.lineEditEmail.text(),
                        self.WindowE.lineEditPhone.text()
                    ])
                    self.WindowE.lineEditFirst.clear()
                    self.WindowE.lineEditLast.clear()
                    self.WindowE.lineEditEmail.clear()
                    self.WindowE.lineEditPhone.clear()
                else:
                    self.WindowE.label_error.setText('Enter a valid email')
            else:
                self.WindowE.label_error.setText('Enter a name')

        elif self.edit == "change":
            index = self.WindowE.comboBox.currentIndex()
            if self.WindowE.lineEditFirst.text():
                if self.email(self.WindowE.lineEditEmail.text()):
                    self.WindowE.label_error.clear()
                    self.originalList[index] = [
                        self.WindowE.lineEditFirst.text(),
                        self.WindowE.lineEditLast.text(),
                        self.WindowE.lineEditEmail.text(),
                        self.WindowE.lineEditPhone.text()]
                else:
                    self.WindowE.label_error.setText('Enter a valid email')
            else:
                self.WindowE.label_error.setText('Enter a name')

            self.fillComboEdit()

        else:
            index = self.WindowE.comboBox.currentIndex()
            self.originalList.pop(index)
            self.fillComboEdit()

        self.save(True)

    def buttonFind(self):
        text = self.WindowF.plainTextEdit.toPlainText()
        phones = ", ".join(re.findall('[#]([0-9]+)', text))
        names = ", ".join(re.findall('[@]([a-zA-Z]+)', text))

        show = 'Names:\n' + names + '\n\nNumbers:\n' + phones
        self.WindowF.plainTextEdit_2.setPlainText(show)

    def buttonAddWeb(self):
        if self.WindowW.lineEditFirst.text():
            if self.email(self.WindowW.lineEditEmail.text()):
                self.WindowW.label_error.clear()
                self.originalList.append([
                    self.WindowW.lineEditFirst.text(),
                    self.WindowW.lineEditLast.text(),
                    self.WindowW.lineEditEmail.text(),
                    self.WindowW.lineEditPhone.text()
                ])
                self.WindowW.lineEditFirst.clear()
                self.WindowW.lineEditLast.clear()
                self.WindowW.lineEditEmail.clear()
                self.WindowW.lineEditPhone.clear()
            else:
                self.WindowW.label_error.setText('Enter a valid email')
        else:
            self.WindowW.label_error.setText('Enter a name')
        self.save(True)

    def buttonGetWeb(self):
        try:
            text = requests.get("https://www.fakenamegenerator.com/", headers={'user-agent': 'my-app/0.0.1'}).text
            sel = Selector(text=text, type='xml')
            oriName = sel.css('#details > div.content > div.info > div > div.address > h3').extract_first().split()
            phone = sel.css('#details > div.content > div.info > div > div.extra > dl:nth-child(5) > dd').extract_first()
            email = sel.css('#details > div.content > div.info > div > div.extra > dl:nth-child(12) > dd').extract_first()

            name = oriName[0].replace("<h3>", "")
            family = oriName[2].replace("</h3>", "")
            phone = phone.replace("<dd>", "").replace("</dd>", "")
            email = email.split()[0].replace("<dd>", "")

            self.WindowW.lineEditFirst.setText(name)
            self.WindowW.lineEditLast.setText(family)
            self.WindowW.lineEditPhone.setText(phone)
            self.WindowW.lineEditEmail.setText(email)
        except:
            self.WindowW.label_error.setText("No Internet Connection")

    def fillTable(self):
        if self.WindowL.radioButtonName.isChecked():
            showList = [i for i in sorted(self.originalList, key=lambda item: item[0])]
        else:
            showList = [i for i in sorted(self.originalList, key=lambda item: item[1])]

        self.WindowL.tableWidget.setRowCount(0)
        for i in range(len(showList)):
            self.WindowL.tableWidget.insertRow(i)
            self.WindowL.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(showList[i][0]))
            self.WindowL.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(showList[i][1]))
            self.WindowL.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(showList[i][2]))
            self.WindowL.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(showList[i][3]))

    def fillComboEdit(self):
        self.WindowE.comboBox.clear()
        self.WindowE.comboBox.addItems([" ".join(i[:2]) for i in self.originalList])

    def fillLineEdit(self):
        index = self.WindowE.comboBox.currentIndex()
        self.WindowE.lineEditFirst.setText(self.originalList[index][0])
        self.WindowE.lineEditLast.setText(self.originalList[index][1])
        self.WindowE.lineEditEmail.setText(self.originalList[index][2])
        self.WindowE.lineEditPhone.setText(self.originalList[index][3])

    def email(self, address):
        if address == "":
            return True
        else:
            regex = '^[0-9a-z]+[\._]?[0-9a-z]+[@][0-9a-z]+[.][0-9a-z]{2,3}$'

            if re.search(regex, address.lower()):
                return True
            else:
                return False

    def open(self):
        try:
            try:
                file = open("myDatabase.txt", 'r')
                self.originalList = json.loads(file.read())
                file.close()
            except:
                self.originalList = []
        except:
            self.originalList = []
            file = open("myDatabase.txt", 'w')
            file.close()

    def save(self, opening=False):
        window = Tk()
        window.withdraw()
        if opening:
            file_name = "myDatabase.txt"
        else:
            file_name = filedialog.asksaveasfilename(title="Save database", initialdir=".\\", initialfile="myDatabase.txt",
                                                     defaultextension="txt", filetypes=(("TXT", "*.txt"), ("JSON", "*.json"), ("XML", "*.xml"), ("All Files", "*.*")))
        if file_name:
            if file_name.lower().endswith(".json"):
                file = open(file_name, 'w')
                json.dump(self.originalList, file)
                file.close()

            elif file_name.lower().endswith(".xml"):
                array = []
                for i in self.originalList:
                    array.append({
                        'name': i[0],
                        'family': i[1],
                        'email': i[2],
                        'phone': i[3],
                    })

                xml = dicttoxml(array, custom_root='Contacts', attr_type=False)
                dom = parseString(xml)
                file = open(file_name, 'w')
                file.write(dom.toprettyxml())
                file.close()

            else:
                file = open(file_name, 'w')
                file.write(json.dumps(self.originalList))
                file.close()

if __name__ == "__main__":
    Application = QtWidgets.QApplication(sys.argv)
    MenuWindow = QtWidgets.QMainWindow()

    program = ConManSys()
    program.setupUi(MenuWindow)
    program.firstStep()

    program.pushButtonEdit.clicked.connect(program.buttonMainEdit)
    program.pushButtonList.clicked.connect(program.buttonMainList)
    program.pushButtonFind.clicked.connect(program.buttonMainFind)
    program.pushButtonWeb.clicked.connect(program.buttonMainWeb)
    program.pushButtonSave.clicked.connect(program.save)

    MenuWindow.show()
    sys.exit(Application.exec_())