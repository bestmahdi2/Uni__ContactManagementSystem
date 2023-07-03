import ast
from lxml import etree
from bs4 import BeautifulSoup
import re
import sys
import json
import requests
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from PyQt5 import QtCore, QtWidgets
from Main import Ui_MainWindow as PMain
from Find import Ui_Dialog as PFind
from Edit import Ui_Dialog as PEdit
from Contacts import Ui_Dialog as PContacts
from Web import Ui_Dialog as PWeb
from Save import Ui_Dialog as PSave

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class RunManager(PMain):
    def setupUi(self, MenuWindow):
        super().setupUi(MenuWindow)

    def retranslateUi(self, MenuWindow):
        super().retranslateUi(MenuWindow)

    def bases(self):
        self.contacts = []
        self.default_load()

    def open_page_contacts(self):
        contacts_app = QtWidgets.QDialog()
        self.PContacts = PContacts()
        self.PContacts.setupUi(contacts_app)
        self.table_update('name')

        self.PContacts.pushButton_name.clicked.connect(lambda x: self.table_update('name'))
        self.PContacts.pushButton_family.clicked.connect(lambda x: self.table_update('family'))
        self.PContacts.pushButton_refresh.clicked.connect(lambda x: self.table_update('name'))

        self.PContacts.pushButton_add.clicked.connect(lambda x: self.open_page_edit('add'))
        self.PContacts.pushButton_change.clicked.connect(lambda x: self.open_page_edit('change'))
        self.PContacts.pushButton_remove.clicked.connect(self.remove_contact)

        contacts_app.show()
        contacts_app.exec_()

    def remove_contact(self):
        index = self.PContacts.tableWidget.currentRow()
        if index >= 0:
            info = [self.PContacts.tableWidget.item(index, 0).text(), self.PContacts.tableWidget.item(index, 1).text(),
                    self.PContacts.tableWidget.item(index, 2).text(), self.PContacts.tableWidget.item(index, 3).text()]
            self.PContacts.label_error1.setText("")
            self.contacts.remove({f'{info[0]} {info[1]}': info})
            self.table_update('name')
            try:
                self.combobox_update()
            except:
                pass

        else:
            self.PContacts.label_error1.setText("Choose a contact from table")

    def open_page_edit(self, state):
        if state == "change" and self.contacts == []:
            self.PContacts.label_error1.setText("No contact to change")
        else:
            self.PContacts.label_error1.setText("")

            edit_app = QtWidgets.QDialog()
            self.PEdit = PEdit()
            self.PEdit.setupUi(edit_app)

            self.combobox_update()
            try:
                self.table_update('name')
            except:
                pass
            self.PEdit.comboBox.currentIndexChanged.connect(self.lineedit_update)

            if state == "add":
                self.PEdit.label_7.setStyleSheet("color:#EB4C42;")
                self.PEdit.comboBox.setStyleSheet("background-color:#EB4C42;color:white")
                self.PEdit.pushButton_do.setText("Add")
                self.PEdit.label_error2.setText("")
                self.PEdit.pushButton_do.clicked.connect(lambda x: self.edit_contacts(state))

            else:
                self.PEdit.comboBox.setCurrentIndex(-1)
                self.PEdit.label_7.setStyleSheet("color:white;")
                self.PEdit.comboBox.setStyleSheet("background-color:#318CE7;color:white")
                self.PEdit.pushButton_do.setText("Change")
                self.PEdit.label_error2.setText("")

                self.PEdit.pushButton_do.clicked.connect(lambda x: self.edit_contacts(state))

            edit_app.show()
            edit_app.exec_()

    def open_page_find(self):
        find_app = QtWidgets.QDialog()
        self.PFind = PFind()
        self.PFind.setupUi(find_app)

        self.PFind.pushButton_dox.clicked.connect(self.seprate_name_phone)

        find_app.show()
        find_app.exec_()

    def edit_contacts(self, state):
        info = [self.PEdit.lineEdit.text(), self.PEdit.lineEdit_2.text(),
                self.PEdit.lineEdit_3.text(), self.PEdit.lineEdit_4.text()]

        if state == "add":
            if info[0] == "":
                self.PEdit.label_error2.setText("Name is empty")
            else:
                self.PEdit.label_error2.setText("")

                if self.email_check(info[3]) == "ok":
                    self.PEdit.label_error2.setText("")
                    self.contacts.append({info[0] + " " + info[1]: info})
                    self.combobox_update()
                    self.PEdit.label_error2.setText("Done!")
                    try:
                        self.table_update('name')
                    except:
                        pass
                else:
                    self.PEdit.label_error2.setText("Invalid email address")

        else:
            if self.PEdit.comboBox.currentIndex() >= 0:
                if info[0] == "":
                    self.PEdit.label_error2.setText("Name is empty")
                else:
                    self.PEdit.label_error2.setText("")

                    if self.email_check(info[3]) == "ok":
                        self.PEdit.label_error2.setText("")
                        self.contacts[self.PEdit.comboBox.currentIndex()] = {info[0] + " " + info[1]: info}
                        self.combobox_update()
                        try:
                            self.table_update('name')
                        except:
                            pass

                    else:
                        self.PEdit.label_error2.setText("Invalid email address")
            else:
                self.PEdit.label_error2.setText("Choose a contact to change")

    def email_check(self, address):
        if address == "":
            return "ok"
        else:
            regex = '^[0-9a-z]+[\._]?[0-9a-z]+[@][0-9a-z]+[.][0-9a-z]{2,3}$'

            if re.search(regex, address.lower().replace(" ", "")):
                return "ok"
            else:
                return "invlaid"

    def table_update(self, state):
        contacts_list = [list(i.values())[0] for i in self.contacts]
        if state == 'name':
            contacts = [i for i in sorted(contacts_list, key=lambda item: item[0])]
        else:
            contacts = [i for i in sorted(contacts_list, key=lambda item: item[1])]

        self.PContacts.tableWidget.setRowCount(0)
        for i in range(0, len(contacts)):
            self.PContacts.tableWidget.insertRow(i)
            self.PContacts.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(contacts[i][0]))
            self.PContacts.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(contacts[i][1]))
            self.PContacts.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(contacts[i][2]))
            self.PContacts.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(contacts[i][3]))

    def combobox_update(self):
        self.PEdit.comboBox.clear()
        if self.contacts != []:
            self.PEdit.comboBox.addItems([list(i.keys())[0] for i in self.contacts])
            index = self.PEdit.comboBox.count()
            self.PEdit.comboBox.setCurrentIndex(index-1)

    def lineedit_update(self):
        index = self.PEdit.comboBox.currentIndex()
        if index >= 0:
            contact_info = list(self.contacts[index].values())[0]
            self.PEdit.lineEdit.setText(contact_info[0])
            self.PEdit.lineEdit_2.setText(contact_info[1])
            self.PEdit.lineEdit_3.setText(contact_info[2])
            self.PEdit.lineEdit_4.setText(contact_info[3])
        else:
            self.PEdit.lineEdit.setText('')
            self.PEdit.lineEdit_2.setText('')
            self.PEdit.lineEdit_3.setText('')
            self.PEdit.lineEdit_4.setText('')

    def seprate_name_phone(self):
        text = self.PFind.textEdit.toPlainText()
        names = re.findall('[@]([\w]+)', text)
        phones = re.findall('[#]([\d]+)', text)

        self.PFind.textBrowser.setText(", ".join(names))
        self.PFind.textBrowser_2.setText(", ".join(phones))

    def open_save_page(self):
        save_app = QtWidgets.QDialog()
        self.PSave = PSave()
        self.PSave.setupUi(save_app)

        self.PSave.pushButton_xml.clicked.connect(lambda x: self.manual_save('xml'))
        self.PSave.pushButton_json.clicked.connect(lambda x: self.manual_save('json'))
        self.PSave.pushButton_txt.clicked.connect(lambda x: self.manual_save('txt'))

        save_app.show()
        save_app.exec_()

    def default_load(self):
        try:
            self.manual_load("txt")
        except:
            try:
                self.manual_save('txt')
            except:
                pass

    def manual_load(self, file):
        if file == "xml":
            pass
        elif file == "json":
            pass
        else:
            self.contacts = []
            with open("contacts.txt", 'r') as f:
                lists = f.readlines()
                tempList = []
                for i in lists:
                    tempList.append(ast.literal_eval(i))

                for i in tempList:
                    self.contacts.append({i[0] + " " + i[1]: i})

    def manual_save(self, file):
        if file == "xml":
            with open("contacts.xml", 'w') as f:
                xml = parseString(dicttoxml(self.contacts, attr_type=False, custom_root='contact'))
                tab = xml.toprettyxml()
                f.write(tab)

        elif file == "json":
            with open("contacts.json", 'w') as f:
                if self.contacts:
                    json.dump(self.contacts, f)
                else:
                    f.write("{}")

        else:
            with open("contacts.txt", 'w') as f:
                tempList = []
                for i in self.contacts:
                    tempList.append(list(i.values())[0])

                list_str = "\n".join([str(i) for i in tempList])
                f.write(list_str)

    def open_page_web(self):
        web_app = QtWidgets.QDialog()
        self.PWeb = PWeb()
        self.PWeb.setupUi(web_app)

        self.PWeb.pushButton_get.clicked.connect(self.get_online_contact)
        self.PWeb.pushButton_add.clicked.connect(self.lineedit_update2)

        web_app.show()
        web_app.exec_()

    def lineedit_update2(self):
        info = [self.PWeb.lineEdit.text(), self.PWeb.lineEdit_2.text(),
                self.PWeb.lineEdit_3.text(), self.PWeb.lineEdit_4.text()]

        if info[0] == "":
            self.PWeb.label_error3.setText("Name is empty")
        else:
            self.PWeb.label_error3.setText("")

            if self.email_check(info[3]) == "ok":
                self.PWeb.label_error3.setText("")
                self.contacts.append({info[0] + " " + info[1]: info})
                self.PWeb.label_error3.setText("Done!")
                try:
                    self.table_update('name')
                except:
                    pass
            else:
                self.PWeb.label_error3.setText("Invalid email address")

    def get_online_contact(self):
        self.PWeb.label_error3.setText("")
        try:
            webpage = requests.get("http://www.fakenamegenerator.com", headers={'User-Agent': 'Chrome'})
            work = etree.HTML(str(BeautifulSoup(webpage.content, "html.parser")))

            name = work.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/h3')[0].text
            family = name.split()[2]
            name = name.split()[0]
            phone = '+1' + work.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[4]/dd/text()')[0]
            email = work.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[9]/dd/text()')[0].replace(" ", "")


            self.PWeb.lineEdit.setText(name)
            self.PWeb.lineEdit_2.setText(family)
            self.PWeb.lineEdit_3.setText(phone)
            self.PWeb.lineEdit_4.setText(email)
        except:
            self.PWeb.label_error3.setText("No connection to internet")


if __name__ == "__main__":
    ori_app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    obj = RunManager()
    obj.setupUi(window)
    obj.bases()

    obj.pushButton_contacts.clicked.connect(obj.open_page_contacts)
    obj.pushButton_web.clicked.connect(obj.open_page_web)
    obj.pushButton_find.clicked.connect(obj.open_page_find)
    obj.pushButton_save.clicked.connect(obj.open_save_page)
    obj.pushButton_load.clicked.connect(obj.manual_load)

    window.show()
    sys.exit(ori_app.exec_())
