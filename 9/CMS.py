from PyQt5 import QtCore, QtWidgets
from myProzhe import Ui_MainWindow
from Text import Ui_Texts
from change import Ui_Change
from List import Ui_List
from Web import Ui_web
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
        uiC = Ui_Change()
        uiC.setupUi(appC)

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

            uiC.label_errorshow.setText("")

            if uiC.radioButton.isChecked():
                if email(uiC.lineEdit_email.text().lower()) == True:
                    adder = {'Name: ': uiC.lineEditName.text().capitalize(),
                             'Family Name: ': uiC.lineEdit_Family.text().capitalize(),
                             'Email Address: ': uiC.lineEdit_email.text(),
                             'Phone Number: ': uiC.lineEdit_phone.text()
                             }

                    myList.append(adder)
                    uiC.lineEdit_id.setText("")
                    uiC.lineEditName.setText("")
                    uiC.lineEdit_Family.setText("")
                    uiC.lineEdit_email.setText("")
                    uiC.lineEdit_phone.setText("")

                else:
                    uiC.label_errorshow.setText("Email Address is invalid !")

            elif uiC.radioButton_2.isChecked():
                if uiC.lineEdit_id.text().isdigit() == False:
                    uiC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif uiC.lineEdit_id.text() == "":
                    uiC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(uiC.lineEdit_id.text()) < len(myList):
                    uiC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    del myList[int(uiC.lineEdit_id.text())]
                    uiC.lineEdit_id.setText("")
                    uiC.lineEditName.setText("")
                    uiC.lineEdit_Family.setText("")
                    uiC.lineEdit_email.setText("")
                    uiC.lineEdit_phone.setText("")

            elif uiC.radioButton_3.isChecked():
                if uiC.lineEdit_id.text().isdigit() == False:
                    uiC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif uiC.lineEdit_id.text() == "":
                    uiC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(uiC.lineEdit_id.text()) < len(myList):
                    uiC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    if email(uiC.lineEdit_email.text().lower()) == True:
                        myList[int(uiC.lineEdit_id.text())] = {'Name: ': uiC.lineEditName.text().capitalize(),
                                 'Family Name: ': uiC.lineEdit_Family.text().capitalize(),
                                 'Email Address: ': uiC.lineEdit_email.text(),
                                 'Phone Number: ': uiC.lineEdit_phone.text()
                                 }

                        uiC.lineEdit_id.setText("")
                        uiC.lineEditName.setText("")
                        uiC.lineEdit_Family.setText("")
                        uiC.lineEdit_email.setText("")
                        uiC.lineEdit_phone.setText("")

                    else:
                        uiC.label_errorshow.setText("Email Address is invalid !")

            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]
            myGlist = myList

        def add():
            uiC.lineEdit_id.setEnabled(False)
            uiC.pushButton_open.setEnabled(False)
            uiC.pushButton.setText("Add")

        def remove():
            uiC.lineEdit_id.setEnabled(True)
            uiC.pushButton_open.setEnabled(True)
            uiC.pushButton.setText("Remove")

        def change():
            uiC.lineEdit_id.setEnabled(True)
            uiC.pushButton_open.setEnabled(True)
            uiC.pushButton.setText("Change")

        def open():
            global myGlist
            myList = myGlist
            myList = [i for i in sorted(myList, key=lambda item: item['Name: '])]

            uiC.label_errorshow.setText("")
            id = uiC.lineEdit_id.text()

            if id != "":
                if uiC.lineEdit_id.text().isdigit() == False:
                    uiC.label_errorshow.setText("Invalid input for id, it should be numberic")
                elif uiC.lineEdit_id.text() == "":
                    uiC.label_errorshow.setText("Enter a id to remove a contact")
                elif not 0 <= int(uiC.lineEdit_id.text()) < len(myList):
                    uiC.label_errorshow.setText("Invalid input for id, can't find such id")
                else:
                    uiC.lineEditName.setText(myList[int(id)]["Name: "])
                    uiC.lineEdit_Family.setText(myList[int(id)]["Family Name: "])
                    uiC.lineEdit_email.setText(myList[int(id)]["Email Address: "])
                    uiC.lineEdit_phone.setText(myList[int(id)]["Phone Number: "])

            else:
                uiC.lineEditName.setText("")
                uiC.lineEdit_Family.setText("")
                uiC.lineEdit_email.setText("")
                uiC.lineEdit_phone.setText("")

        uiC.lineEdit_id.setEnabled(False)
        uiC.pushButton_open.setEnabled(False)
        uiC.radioButton.clicked.connect(add)
        uiC.radioButton_2.clicked.connect(remove)
        uiC.radioButton_3.clicked.connect(change)
        uiC.pushButton.clicked.connect(saveClicked)
        uiC.pushButton_open.clicked.connect(open)

        appC.show()
        appC.exec_()

    def ListContacts(self):
        self.label_done.setText("")
        global myGlist
        appL = QtWidgets.QDialog()
        uiL = Ui_List()
        uiL.setupUi(appL)

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

            uiL.textBrowser.setText("\n\n".join(printer))

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

            uiL.textBrowser.setText("\n\n".join(printer))

        name_sort()
        uiL.radioButton_name.clicked.connect(name_sort)
        uiL.radioButton_Family.clicked.connect(family_sost)

        appL.show()
        appL.exec_()

    def Web(self):
        self.label_done.setText("")
        global myGlist
        self.label_done.setText("")
        appW = QtWidgets.QDialog()
        uiW = Ui_web()
        uiW.setupUi(appW)

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

            uiW.label_errorshow.setText("")

            if email(uiW.lineEdit_email.text().lower()) == True:
                adder = {'Name: ': uiW.lineEditName.text().capitalize(),
                         'Family Name: ': uiW.lineEdit_Family.text().capitalize(),
                         'Email Address: ': uiW.lineEdit_email.text(),
                         'Phone Number: ': uiW.lineEdit_phone.text()
                         }

                myList.append(adder)
                uiW.lineEditName.setText("")
                uiW.lineEdit_Family.setText("")
                uiW.lineEdit_email.setText("")
                uiW.lineEdit_phone.setText("")

            else:
                uiW.label_errorshow.setText("Email Address is invalid !")

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
                uiW.label_errorshow.setText("")
                uiW.lineEditName.setText(myList[0])
                uiW.lineEdit_Family.setText(myList[1])
                uiW.lineEdit_email.setText(myList[2])
                uiW.lineEdit_phone.setText(myList[3])
            else:
                uiW.label_errorshow.setText("Internet Connection Lost.")

        uiW.pushButton.clicked.connect(saveClicked)
        uiW.pushButton_2.clicked.connect(getData)

        appW.show()
        appW.exec_()

    def Text(self):
        self.label_done.setText("")
        appT = QtWidgets.QDialog()
        uiT = Ui_Texts()
        uiT.setupUi(appT)

        def NamePhone():
            text = uiT.textEdit.toPlainText()

            phones = re.findall('[#]+([0-9]+)', text)
            names = re.findall('[@]+([A-Za-z]+)', text)

            if names == []:
                names = ["No names !"]
            if phones == []:
                phones = ["No phones !"]

            printer = "Names:\n" + "\n".join(names) + "\n\nPhones:\n" + "\n".join(phones)

            uiT.textBrowser.setText(printer)

        uiT.pushButton.clicked.connect(NamePhone)

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

ui = CMS()
ui.setupUi(MainWindow)
ui.Load()

ui.pushButton_change.clicked.connect(ui.ChangeContacts)
ui.pushButton_contacts.clicked.connect(ui.ListContacts)

ui.pushButton_txt.clicked.connect(ui.TXTfile)
ui.pushButton_json.clicked.connect(ui.JSONfile)

ui.pushButton_find.clicked.connect(ui.Text)
ui.pushButton_web.clicked.connect(ui.Web)

MainWindow.show()
sys.exit(app.exec_())
