import re
import sqlite3
import sys
import json
from bs4 import BeautifulSoup
from lxml import etree
from requests import get
from random import randint
from PyQt5 import QtCore, QtWidgets, QtGui
from mainwin import Ui_MainWindow as Window

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainClass(Window):
    def setupUi(self, Main):
        super().setupUi(Main)

        self.ContactsList = []

        photo = QtGui.QPixmap('Photo.png')
        self.labelPhoto.setPixmap(photo)

        self.label_version.setText("1.0.8")

        self.pushButtonAdd.clicked.connect(self.addContact)
        self.pushButtonDelete.clicked.connect(self.deleteContact)
        self.pushButtonUpdate.clicked.connect(self.updateContact)
        self.comboBoxContact.currentIndexChanged.connect(self.InputContact)
        self.lineEditEmail.textChanged.connect(self.CheckEmail)
        self.lineEditPhone.textChanged.connect(self.CheckPhone)

        self.lineEditSearch.textChanged.connect(self.search)
        self.pushButtonName.clicked.connect(self.sortName)
        self.pushButtonFamily.clicked.connect(self.sortFamily)

        self.pushButtonCrawl.clicked.connect(self.crawl)

        self.pushButtonScrap.clicked.connect(self.scrap)
        self.pushButtonUse.clicked.connect(self.use)

        self.pushButtonSQLSave.clicked.connect(self.saveSqlite)
        self.pushButtonSQLRead.clicked.connect(self.readSqlite)
        self.pushButtonTXTSave.clicked.connect(self.saveTXT)
        self.pushButtonTXTRead.clicked.connect(self.readTXT)

    def retranslateUi(self, Main):
        super().retranslateUi(Main)

    def addContact(self):
        if self.lineEditName.text():
            self.error.clear()
            first_name = self.lineEditName.text()
            last_name = self.lineEditFamily.text()
            phone_number = self.lineEditPhone.text()
            email_address = self.lineEditEmail.text()

            temp = {'name': first_name, 'family': last_name, 'phone': phone_number, 'email': email_address}

            if temp not in self.ContactsList:
                self.ContactsList.append(temp)
                self.fillCombo()
                self.table()
                self.empty1()
            else:
                self.error.setText("Duplicated Contact !")
        else:
            self.error.setText("Name is empty !")

    def deleteContact(self):
        if self.comboBoxContact.currentIndex() == -1:
            self.error.setText("Please select a contact !")
        else:
            self.ContactsList.pop(self.comboBoxContact.currentIndex())
            self.error.clear()
            self.fillCombo()
            self.table()
            self.empty1()

    def updateContact(self):
        if self.comboBoxContact.currentIndex() == -1:
            self.error.setText("Please select a contact !")

        else:
            if self.lineEditName.text():
                self.error.clear()
                first_name = self.lineEditName.text()
                last_name = self.lineEditFamily.text()
                phone_number = self.lineEditPhone.text()
                email_address = self.lineEditEmail.text()

                temp = {'name': first_name, 'family': last_name, 'phone': phone_number, 'email': email_address}

                if temp not in self.ContactsList:
                    self.ContactsList[self.comboBoxContact.currentIndex()] = temp
                    self.fillCombo()
                    self.table()
                    self.empty1()
                else:
                    self.error.setText("Duplicated Contact !")
            else:
                self.error.setText("Name is empty !")

    def empty1(self):
        self.lineEditName.clear()
        self.lineEditFamily.clear()
        self.lineEditPhone.clear()
        self.lineEditEmail.clear()

    def fillCombo(self):
        self.comboBoxContact.clear()
        self.comboBoxContact.addItems([f'{i["name"]}, {i["family"]}' for i in self.ContactsList])
        self.comboBoxContact.setCurrentIndex(-1)

    def InputContact(self):
        if self.comboBoxContact.currentIndex() != -1:
            contact = self.ContactsList[self.comboBoxContact.currentIndex()]
            self.lineEditName.setText(contact['name'])
            self.lineEditFamily.setText(contact['family'])
            self.lineEditPhone.setText(contact['phone'])
            self.lineEditEmail.setText(contact['email'])

    def CheckEmail(self):
        text = self.lineEditEmail.text().lower()
        regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if text == "" or re.search(regex, text):
            self.pushButtonUpdate.setEnabled(True)
            self.pushButtonAdd.setEnabled(True)
            self.error.clear()

        else:
            self.pushButtonUpdate.setEnabled(False)
            self.pushButtonAdd.setEnabled(False)
            self.error.setText("Email address invalid !")

    def CheckPhone(self):
        numbers = self.lineEditPhone.text()
        if numbers == "" or numbers.isdigit():
            self.pushButtonUpdate.setEnabled(True)
            self.pushButtonAdd.setEnabled(True)
            self.error.clear()

        else:
            self.pushButtonUpdate.setEnabled(False)
            self.pushButtonAdd.setEnabled(False)
            self.error.setText("Phone number invalid !")

    def search(self):
        self.tableWidget.setRowCount(0)

        found = []
        searching = self.lineEditSearch.text()
        for i in self.ContactsList:
            for j in [j.lower() for j in i.values()]:
                if searching.lower() in j:
                    if i not in found:
                        found.append(i)

        i = 0
        while i < len(found):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(found[i]['name']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(found[i]['family']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(found[i]['phone']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(found[i]['email']))
            i += 1

    def sortName(self):
        self.table('name')

    def sortFamily(self):
        self.table('family')

    def table(self, sorting='name'):
        self.tableWidget.setRowCount(0)

        sort = [i for i in sorted(self.ContactsList, key=lambda obj: obj[sorting])]

        i = 0
        while i < len(sort):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(sort[i]['name']))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(sort[i]['family']))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(sort[i]['phone']))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(sort[i]['email']))
            i += 1

    def crawl(self):
        self.textBrowser_2.setText("\n".join(re.findall('[@]([a-zA-Z]+)', self.textBrowser.toPlainText())))
        self.textBrowser_3.setText("\n".join(re.findall('[#]([0-9]+)', self.textBrowser.toPlainText())))

    def scrap(self):
        site = self.comboBoxSite.currentIndex()
        name, family, phone, email = "", "", "", ""

        if site == 0:
            self.error_2.setVisible(False)

            site = "https://www.fakenamegenerator.com/"

            try:
                webpage = get(site, headers={'User-Agent': 'mOMIDs'})
                soup = BeautifulSoup(webpage.content, "html.parser")
                dom = etree.HTML(str(soup))

                name = dom.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/h3')[0].text
                family = name.split()[-1]
                name = name.replace(f' {family}', "")
                phone = dom.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[4]/dd/text()')[0].replace("-", "")
                email = dom.xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/dl[9]/dd/text()')[0].replace(" ", "")

            except:
                self.error_2.setVisible(True)
                self.error_2.setText("Inter Problem Detected !")

        else:
            self.error_2.setVisible(False)

            random_contact = str(randint(10001, 99999))

            site = "https://www.random-name-generator.com/united-states?gender=&n=1&s=" + random_contact

            try:
                webpage = get(site, headers={'User-Agent': 'mOMIDs'})
                soup = BeautifulSoup(webpage.content, "html.parser")
                dom = etree.HTML(str(soup))

                name = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[1]/text()')[0].split()[0]
                family = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[1]/text()')[0].split()[
                    1]
                phone = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[1]/dd[3]/text()')[0]
                phone = phone.replace("(", "").replace(") ", "").replace("+1", "").split()[0].replace("-", " ").replace(
                    ".", " ").replace(" ", "")
                email = dom.xpath('/html/body/div/div[4]/div[2]/div/div/div[5]/div/div/dl[2]/dd[1]/text()')[0].replace(
                    "\n", "")

            except:
                self.error_2.setVisible(True)
                self.error_2.setText("Inter Problem Detected !")

        self.lineEditName_2.setText(name)
        self.lineEditFamily_2.setText(family)
        self.lineEditPhone_2.setText(phone)
        self.lineEditEmail_2.setText(email)

    def use(self):
        self.error.clear()
        first_name = self.lineEditName_2.text()
        last_name = self.lineEditFamily_2.text()
        phone_number = self.lineEditPhone_2.text()
        email_address = self.lineEditEmail_2.text()

        temp = {'name': first_name, 'family': last_name, 'phone': phone_number, 'email': email_address}

        if temp not in self.ContactsList:
            self.ContactsList.append(temp)
            self.fillCombo()
            self.table()
            self.empty1()
            self.lineEditName_2.clear()
            self.lineEditFamily_2.clear()
            self.lineEditPhone_2.clear()
            self.lineEditEmail_2.clear()

        else:
            self.error_2.setText("Duplicated Contact !")

    def saveSqlite(self):
        def create_connection(db_file):
            try:
                with open(db_file, "r") as file:
                    pass
            except:
                with open(db_file, "w") as file:
                    pass

            conn = None
            try:
                conn = sqlite3.connect(db_file)
                return conn
            except:
                pass

            return conn

        # create a database connection
        conn = create_connection("Database.db")

        # create tables
        create_table_exe = """ CREATE TABLE IF NOT EXISTS Contacts (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            family text,
                                            email text,
                                            phone text
                                        ); """
        c = conn.cursor()
        c.execute(create_table_exe)

        # delete data
        sql = 'DELETE FROM Contacts'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        # insert data
        if self.ContactsList:
            for i in self.ContactsList:
                sql = ''' INSERT INTO Contacts(name,family,phone,email)
                              VALUES(?,?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, list(i.values()))
                conn.commit()

        self.error_3.setText("Sqlite Saved. !")

    def readSqlite(self):
        ok = False
        self.error_3.clear()
        try:
            with open("Database.db", "r") as file:
                ok = True
            self.error_3.setText("Sqlite loaded into program.")

        except:
            self.error_3.setText("No sqlite database were found in directory.")

        if ok:
            def create_connection(db_file):
                conn = None
                try:
                    conn = sqlite3.connect(db_file)
                    return conn
                except:
                    pass

                return conn

            # create a database connection
            conn = create_connection("Database.db")

            # read data
            cur = conn.cursor()
            cur.execute("SELECT * FROM Contacts")
            rows = cur.fetchall()
            self.ContactsList = []
            for row in rows:
                temp = {'name': row[1], 'family': row[2], 'phone': row[4], 'email': row[3]}
                self.ContactsList.append(temp)

        self.table()

    def saveTXT(self):
        with open("Database.txt", 'w') as file:
            file.write(json.dumps(self.ContactsList))

        self.error_3.setText("TXT Saved. !")

    def readTXT(self):
        try:
            with open("Database.txt", 'r') as file:
                self.ContactsList = json.loads(file.read())
                self.error_3.setText("TXT loaded into program.")
        except:
            self.error_3.setText("No TXT database were found in directory. A new One Created.")
            with open("Database.txt", 'w') as file:
                pass

        self.table()


if __name__ == "__main__":
    CMSApp = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()

    Class = MainClass()
    Class.setupUi(Window)
    Class.readTXT()
    Class.table()
    Class.fillCombo()
    Class.empty1()

    Window.show()
    sys.exit(CMSApp.exec_())
