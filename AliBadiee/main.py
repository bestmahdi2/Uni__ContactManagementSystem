from PyQt5.QtGui import QPixmap
from ProgramFile.ProcessPart import CMSDictProcess, CMSTextProcess
from ProgramFile.ContactManagementSystem import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from os import sep, getcwd

# Hidpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# use Hidpi icons
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class CMS(Ui_MainWindow):
    def setupUi(self, MainWindow):
        """CMS_UI parent class function"""

        super().setupUi(MainWindow)

        # region icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Contacts.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        # endregion

    def retranslateUi(self, MainWindow):
        """CMS_UI parent class function"""

        super().retranslateUi(MainWindow)
        _translate = QtCore.QCoreApplication.translate

    def main(self, mode="") -> None:
        """Main function"""

        pixmap = QPixmap('Profile.png')
        self.Label_Master.setPixmap(pixmap)

        T = CMSTextProcess()

        if mode == "newDatabase":
            database_loc = self.comboBox.currentText()
        else:
            database_loc = f'{getcwd()}{sep}Databases{sep}Contacts.txt'

        self.comboBox.setCurrentText(database_loc)
        self.comboBox.addItem(database_loc)

        dicts = T.FileToDict(self.comboBox.currentText())
        if dicts != False:
            self.dict = dicts
            self.comboBox_contacts.addItems(self.Listing(self.dict))
            self.Error.setStyleSheet("color:#FDF57A")
            self.Error_2.setStyleSheet("color:#FDF57A")
            self.Error.setText("")
            self.Error_2.setText("")
            self.FillLineEditsTab0()
            self.FillTableTab2()
        else:
            self.dict = {}
            self.Error.setStyleSheet("color:#EB4C42")
            self.Error_2.setStyleSheet("color:#EB4C42")
            self.Error.setText("Invalid database")
            self.Error_2.setText("Invalid database")

    def closeEvent(self, event) -> None:
        """This function enables when user close the main window"""

        T = CMSTextProcess()
        if T.FileToDict(self.comboBox.currentText()) != self.dict:
            reply = QtWidgets.QMessageBox.question(MainWindow, 'Close Without Saving ???',
                                                   'Do you want to save contacts changes to database? ',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    T.DictToFile(self.comboBox.currentText(), self.dict)
                    QtWidgets.QMessageBox.information(MainWindow, "Done !!!",
                                                  "Contacts changes saved to database successfully !")

                except:
                    QtWidgets.QMessageBox.information(MainWindow, "Saving failed !!!",
                                                  "Unfortunately couldn't save contacts "
                                                  "changes to database !")
                event.accept()
            else:
                event.accept()

    def Date(self) -> None:
        """This function gets the data from api"""

        import requests
        url = "https://api.keybit.ir/time/"
        try:
            QtWidgets.QApplication.processEvents()
            dicts = requests.get(url).json()
            self.Label_date.setText(dicts["date"]["full"]["official"]["usual"]["en"])
        except:
            from persiantools.jdatetime import JalaliDate
            self.Label_date.setText(str(JalaliDate.today()).replace("-", "/"))
            self.Label_Done.setText("Something wrong with internet connection")

    # region tabs
    def CleanEditLines(self) -> None:
        """This function clears the lineEdits and Error labels text"""

        self.Label_Done.setText("")
        if self.tabWidget.currentIndex() == 0:
            self.Error.setText("")
            self.comboBox_contacts.setCurrentIndex(-1)
            self.lineEdit_first.setText("")
            self.lineEdit_last.setText("")
            self.lineEdit_phone.setText("")
            self.lineEdit_email.setText("")
            self.lineEdit_notes.setText("")

        if self.tabWidget.currentIndex() == 1:
            self.Error_2.setText("")
            self.lineEdit_first_2.setText("")
            self.lineEdit_last_2.setText("")
            self.lineEdit_phone_2.setText("")
            self.lineEdit_email_2.setText("")
            self.lineEdit_notes_2.setText("")

    def NewDatabase(self) -> None:
        """This function opens new database"""

        self.comboBox_contacts.clear()
        self.lineEdit_first.setText("")
        self.lineEdit_last.setText("")
        self.lineEdit_phone.setText("")
        self.lineEdit_email.setText("")
        self.lineEdit_notes.setText("")
        self.lineEdit_first_2.setText("")
        self.lineEdit_last_2.setText("")
        self.lineEdit_phone_2.setText("")
        self.lineEdit_email_2.setText("")
        self.lineEdit_notes_2.setText("")
        self.lineEdit_searchby.setText("")
        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)
        if self.comboBox.currentText():
            self.Error.setStyleSheet("color:#FDF57A")
            self.Error_2.setStyleSheet("color:#FDF57A")
            self.Error.setText("")
            self.Error_2.setText("")
            self.main("newDatabase")

        else:
            self.Error.setStyleSheet("color:#EB4C42")
            self.Error_2.setStyleSheet("color:#EB4C42")
            self.Error.setText("Empty address box")
            self.Error_2.setText("Empty address box")

    # tab 0
    @staticmethod
    def Listing(dicts: dict) -> list:
        """This function gets a dictionary,
        creates a list of contacts in the dictionary
        returns the list"""

        contacts = []
        for i in list(dicts.values()):
            contacts.append(f'{i["firstName"]} {i["lastName"]}')
        return contacts

    def FillLineEditsTab0(self) -> None:
        """This function fills LineEdits in tab 0"""

        index = self.comboBox_contacts.currentIndex()
        if index >= 0:
            items = self.dict[str(index + 1)]
            self.lineEdit_first.setText(items['firstName'])
            self.lineEdit_last.setText(items['lastName'])
            self.lineEdit_phone.setText(items['phone'])
            self.lineEdit_email.setText(items['email'])
            self.lineEdit_notes.setText(items['extras'])

    # tab 1
    def SearchBy(self) -> None:
        """This function sort the table items by data in lineEdit and combobox"""

        search = self.lineEdit_searchby.text().lower()
        if search:
            self.tableWidget.setRowCount(0)
            index = self.comboBox_search.currentIndex()
            translate = {0: "firstName", 1: "lastName", 2: "phone", 3: "email"}

            P = CMSDictProcess()
            founds = P.FindContact(self.dict, translate[index], search)

            x = 0
            while x < len(founds):
                self.tableWidget.insertRow(x)
                items = f'{founds[x]}) ' + ", ".join(list(self.dict[str(founds[x])].values()))
                self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(items))
                x += 1

    def FillLineEditsTab1(self) -> None:
        """This function fills LineEdits in tab 1"""

        try:
            index = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()[0])
            if index >= 0:
                items = self.dict[str(index)]
                self.lineEdit_first_2.setText(items['firstName'])
                self.lineEdit_last_2.setText(items['lastName'])
                self.lineEdit_phone_2.setText(items['phone'])
                self.lineEdit_email_2.setText(items['email'])
                self.lineEdit_notes_2.setText(items['extras'])
        except:
            pass

    # tab 2
    def FillTableTab2(self) -> None:
        """This function fills table in tab 2"""

        self.tableWidget_2.setRowCount(0)
        if self.dict:
            index = self.comboBox_sort.currentIndex()
            translate = {0: "firstName", 1: "lastName", 2: "phone", 3: "email"}

            P = CMSDictProcess()
            dicts = P.SortContact(self.dict, translate[index])
            founds = []

            for i in list(dicts.keys()):
                text = ", ".join(list(dicts[i].values()))
                founds.append(text)

            x = 0
            while x < len(founds):
                self.tableWidget_2.insertRow(x)
                self.tableWidget_2.setItem(x, 0, QtWidgets.QTableWidgetItem(founds[x]))
                x += 1

    def SwitchToTab2(self) -> None:
        self.tabWidget.setCurrentIndex(2)
        self.FillTableTab2()

    # tab 3, 4
    def SwitchTab(self) -> None:
        """This function handle changes when switching between tabs"""

        if self.tabWidget.currentIndex() == 3 or self.tabWidget.currentIndex() == 4:
            font = QtGui.QFont()
            font.setFamily("Calibri"), font.setPointSize(12)
            font.setBold(False), font.setWeight(50)
            self.Button_SaveAs.setFont(font)

            self.Button_Save.setText("📚 Copy")

            if self.tabWidget.currentIndex() == 3:
                self.Button_Save.setStatusTip("Copy Names and Phones")
                self.Button_SaveAs.setStatusTip("Clear Boxes")
                self.Button_SaveAs.setText("🧹 Clear")

            else:
                self.Button_Save.setStatusTip("Copy Contact Info")
                self.Button_SaveAs.setStatusTip("Use This Contact In Program")
                self.Button_SaveAs.setText("🛠 Use")

            self.groupBox_Loc.setVisible(False)
            self.Button_Contacts.setVisible(False)

            self.Label_Done.setGeometry(QtCore.QRect(630, 140, 81, 111))

        else:
            self.Button_Save.setStatusTip("Save contacts changes to database")
            self.Button_Save.setText("💾 Save")
            font = QtGui.QFont()
            font.setFamily("Calibri"), font.setPointSize(9)
            font.setBold(False), font.setWeight(50)
            self.Button_SaveAs.setFont(font)
            self.Button_SaveAs.setStatusTip("Save database as json, xml")
            self.Button_SaveAs.setText("💾 Save As")

            self.groupBox_Loc.setVisible(True)
            self.Button_Contacts.setVisible(True)

            self.Label_Done.setGeometry(QtCore.QRect(630, 190, 81, 111))

    # endregion

    # region Buttons
    def ButtonOpen(self) -> None:
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select Files", initialdir="./",
                                               filetypes=(("TEXT", "*.txt"), ("All Files", "*.*")))

        file_path = str(file_path).replace("/", sep).replace("\\", sep)
        self.comboBox.setStyleSheet("color:yellow;")
        self.comboBox.setCurrentText(file_path)
        self.comboBox.addItem(file_path)

    def ButtonSave(self) -> None:
        T = CMSTextProcess()
        if self.tabWidget.currentIndex() == 3 or self.tabWidget.currentIndex() == 4:
            from pyperclip import copy
            text = ""

            if self.tabWidget.currentIndex() == 3:
                text = f'Names:\n{self.textBrowser_names.toPlainText()}\n\nPhones:\n{self.textBrowser_phones.toPlainText()}'
                self.Label_Done.setText("Names and phones copied to clipboard")

            else:
                info = [self.lineEdit_first_3.text(), self.lineEdit_last_3.text(),
                        self.lineEdit_phone_3.text(), self.lineEdit_email_3.text()]

                if list(set(info)) != ['']:
                    text = f'First Name:\n{info[0]}\n\n' + \
                           f'Last Name:\n{info[1]}\n\n' + \
                           f'Phone Number:\n{info[2]}\n\n' + \
                           f'Email Address:\n{info[3]}'

                    self.Label_Done.setText("Cantact info copied to clipboard")

                else:
                    self.Label_Done.setText("No cantact selected to copy")

            copy(text)

        else:
            T.DictToFile(self.comboBox.currentText(), self.dict)
            self.Label_Done.setText("Contacts saved to database successfully")

    def ButtonSaveAs(self) -> None:
        if self.tabWidget.currentIndex() == 3:
            self.textEdit.setText("")
            self.textBrowser_names.setText("")
            self.textBrowser_phones.setText("")

        elif self.tabWidget.currentIndex() == 4:
            T = CMSTextProcess()

            info = [self.lineEdit_first_3.text(), self.lineEdit_last_3.text(),
                    self.lineEdit_phone_3.text(), self.lineEdit_email_3.text()]

            if list(set(info)) != ['']:
                self.Error_3.setText("")
                self.tabWidget.setCurrentIndex(0)
                self.comboBox_contacts.setCurrentIndex(-1)
                self.lineEdit_first.setText(info[0])
                self.lineEdit_last.setText(info[1])
                self.lineEdit_phone.setText(info[2])
                self.lineEdit_email.setText(info[3])
            else:
                self.Error_3.setStyleSheet("color:#EB4C42")
                self.Error_3.setText("No Contact Selected")

        else:
            T = CMSTextProcess()
            T.DictToJsonXml(self.dict)

    def ButtonDelete(self) -> None:
        T = CMSTextProcess()
        T.DictToFile(self.comboBox.currentText(), {})
        self.Label_Done.setText("Contacts deleted from database successfully")

    def ButtonProcess(self) -> None:
        T = CMSTextProcess()
        text = self.textEdit.toPlainText()
        text_processed = T.TextCrawler(text)
        names, phones = "\n".join(text_processed[0]), "\n".join(text_processed[1])

        if names:
            self.textBrowser_names.setText(names)
        else:
            self.textBrowser_names.setText("No names were found.")
        if phones:
            self.textBrowser_phones.setText(phones)
        else:
            self.textBrowser_phones.setText("No phones were found.")

    def ButtonAdd(self) -> None:
        P = CMSDictProcess()
        T = CMSTextProcess()
        errors = []
        warnings = []
        no_error = True
        tab_index = self.tabWidget.currentIndex()

        if tab_index == 0:
            temp_dic = [self.lineEdit_first.text(), self.lineEdit_last.text(), self.lineEdit_phone.text(),
                        self.lineEdit_email.text(), self.lineEdit_notes.text()]
        else:
            temp_dic = [self.lineEdit_first_2.text(), self.lineEdit_last_2.text(), self.lineEdit_phone_2.text(),
                        self.lineEdit_email_2.text(), self.lineEdit_notes_2.text()]

        if not temp_dic[0]:
            errors.append("First name is necessary")
            no_error = False

        if temp_dic[3] and not T.EmailVerification(temp_dic[3]):
            errors.append("Invalid email Address")
            no_error = False

        if not temp_dic[1]:
            warnings.append("Last name")
        if not temp_dic[2]:
            warnings.append("Phone number")
        if not temp_dic[3]:
            warnings.append("Email Address")

        if no_error:
            dicts = P.CreateContact(self.dict, temp_dic)
            if isinstance(dicts, bool):
                if tab_index == 0:
                    self.Error.setStyleSheet("color:#EB4C42")
                    self.Error.setText("Contact is already in database")
                else:
                    self.Error_2.setStyleSheet("color:#EB4C42")
                    self.Error_2.setText("Contact is already in database")
            else:
                self.dict = dicts
                if tab_index == 0:
                    self.comboBox_contacts.clear()
                    self.Error.clear()
                    self.comboBox_contacts.addItems(self.Listing(self.dict))
                    self.comboBox_contacts.setCurrentIndex(int(list(self.dict.keys())[-1]) - 1)
                    if warnings:
                        text = "Empty Boxes: " + ", ".join(warnings)
                        self.Error.setStyleSheet("color:#FDF57A")
                        self.Error.setText(text)
                else:
                    self.Error_2.clear()
                    self.tableWidget.setRowCount(0)
                    self.lineEdit_searchby.setText("")
                    if warnings:
                        text = "Empty Boxes: " + ", ".join(warnings)
                        self.Error_2.setStyleSheet("color:#FDF57A")
                        self.Error_2.setText(text)

        else:
            if tab_index == 0:
                self.Error.setStyleSheet("color:#EB4C42")
                self.Error.setText(errors[0])
            else:
                self.Error_2.setStyleSheet("color:#EB4C42")
                self.Error_2.setText(errors[0])

    def ButtonRemove(self) -> None:
        tab_index = self.tabWidget.currentIndex()
        P = CMSDictProcess()
        index = False

        if tab_index == 0:
            index = self.comboBox_contacts.currentIndex() + 1
            self.comboBox_contacts.removeItem(index)
        else:
            try:
                index = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()[0])
            except AttributeError:
                self.Error_2.setStyleSheet("color:#EB4C42")
                self.Error_2.setText("No Contact Selected")

        if index != False:
            self.dict = P.DeleteContact(self.dict, str(index))

            if tab_index == 0:
                self.comboBox_contacts.clear()
                self.comboBox_contacts.addItems(self.Listing(self.dict))
                self.comboBox_contacts.setCurrentIndex(0)
            else:
                self.tableWidget.setRowCount(0)
                self.lineEdit_searchby.setText("")

            self.CleanEditLines()

    def ButtonChange(self) -> None:
        tab_index = self.tabWidget.currentIndex()
        T = CMSTextProcess()
        P = CMSDictProcess()
        errors = []
        warnings = []
        no_error = True

        if tab_index == 0:
            if self.comboBox_contacts.currentIndex() >= 0:
                temp_dic = [self.lineEdit_first.text(), self.lineEdit_last.text(), self.lineEdit_phone.text(),
                            self.lineEdit_email.text(), self.lineEdit_notes.text()]

                if not temp_dic[0]:
                    errors.append("First name is necessary")
                    no_error = False

                if temp_dic[3] and not T.EmailVerification(temp_dic[3]):
                    errors.append("Invalid email Address")
                    no_error = False

                if not temp_dic[1]:
                    warnings.append("Last name")
                if not temp_dic[2]:
                    warnings.append("Phone number")
                if not temp_dic[3]:
                    warnings.append("Email Address")

                if no_error:
                    index = self.comboBox_contacts.currentIndex()

                    dicts = P.EditContact(self.dict, str(index + 1), temp_dic)
                    if isinstance(dicts, bool):
                        self.Error.setStyleSheet("color:#EB4C42")
                        self.Error.setText("A contact is with this info is in database")
                    else:
                        self.dict = dicts
                        self.Error.clear()
                        self.comboBox_contacts.clear()
                        self.comboBox_contacts.addItems(self.Listing(self.dict))
                        self.comboBox_contacts.setCurrentIndex(index)
                        if warnings:
                            text = "Empty Boxes: " + ", ".join(warnings)
                            self.Error.setStyleSheet("color:#FDF57A")
                            self.Error.setText(text)

                else:
                    self.Error.setStyleSheet("color:#EB4C42")
                    self.Error.setText(errors[0])
            else:
                self.Error.setStyleSheet("color:#EB4C42")
                self.Error.setText("Can't Change Uncreated Contact !")
        else:
            temp_dic = [self.lineEdit_first_2.text(), self.lineEdit_last_2.text(), self.lineEdit_phone_2.text(),
                        self.lineEdit_email_2.text(), self.lineEdit_notes_2.text()]

            if not temp_dic[0]:
                errors.append("First name is necessary")
                no_error = False
            if temp_dic[3] and not T.EmailVerification(temp_dic[3]):
                errors.append("Invalid email Address")
                no_error = False
            if not temp_dic[1]:
                warnings.append("Last name")
            if not temp_dic[2]:
                warnings.append("Phone number")
            if not temp_dic[3]:
                warnings.append("Email Address")

            if no_error:
                index = False
                try:
                    index = int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()[0])
                except AttributeError:
                    self.Error_2.setStyleSheet("color:#EB4C42")
                    self.Error_2.setText("No Contact Selected")

                if index != False:
                    dicts = P.EditContact(self.dict, str(index), temp_dic)
                    if isinstance(dicts, bool):
                        self.Error_2.setStyleSheet("color:#EB4C42")
                        self.Error_2.setText("A contact is with this info is in database")
                    else:
                        self.dict = dicts
                        self.Error_2.clear()
                        self.tableWidget.setRowCount(0)
                        self.lineEdit_searchby.setText("")
                        if warnings:
                            text = "Empty Boxes: " + ", ".join(warnings)
                            self.Error_2.setStyleSheet("color:#FDF57A")
                            self.Error_2.setText(text)

            else:
                self.Error_2.setStyleSheet("color:#EB4C42")
                self.Error_2.setText(errors[0])

    def ButtonProcess2(self) -> None:
        self.Label_Done.setText("")
        self.Error_3.setStyleSheet("color:#FDF57A")
        self.Error_3.setText("Processing ...")

        T = CMSTextProcess()
        QtWidgets.QApplication.processEvents()
        data = T.WebScraping()

        if isinstance(data, bool):
            self.Error_3.setText("")
            self.Label_Done.setText("Something wrong with internet connection")
        else:
            self.Error_3.setStyleSheet("color:#FDF57A")
            self.Error_3.setText("Done !")
            self.lineEdit_first_3.setText(data[0])
            self.lineEdit_last_3.setText(data[1])
            self.lineEdit_phone_3.setText(data[2])
            self.lineEdit_email_3.setText(data[3])

    # endregion


if __name__ == "__main__":
    import sys

    version = "1.0.4"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    MainWindow = QtWidgets.QMainWindow()

    ui = CMS()
    ui.setupUi(MainWindow)

    ui.Date()
    ui.main()

    # region main
    MainWindow.closeEvent = ui.closeEvent
    ui.Button_open.clicked.connect(ui.ButtonOpen)
    ui.Button_Save.clicked.connect(ui.ButtonSave)
    ui.Button_Delete.clicked.connect(ui.ButtonDelete)
    ui.Button_Contacts.clicked.connect(ui.SwitchToTab2)
    ui.Button_open_file.clicked.connect(ui.NewDatabase)
    ui.Button_SaveAs.clicked.connect(ui.ButtonSaveAs)
    ui.tabWidget.currentChanged.connect(ui.SwitchTab)
    ui.Label_Master.setStatusTip(f"Version : {version}")
    # endregion

    # region tabs
    # tab 0
    ui.Button_add.clicked.connect(ui.ButtonAdd)
    ui.Button_remove.clicked.connect(ui.ButtonRemove)
    ui.Button_change.clicked.connect(ui.ButtonChange)
    ui.Button_clear.clicked.connect(ui.CleanEditLines)
    ui.comboBox_contacts.currentIndexChanged.connect(ui.FillLineEditsTab0)
    # tab 1
    ui.Button_add_2.clicked.connect(ui.ButtonAdd)
    ui.Button_remove_2.clicked.connect(ui.ButtonRemove)
    ui.Button_change_2.clicked.connect(ui.ButtonChange)
    ui.Button_clear_2.clicked.connect(ui.CleanEditLines)
    ui.tableWidget.itemSelectionChanged.connect(ui.FillLineEditsTab1)
    ui.comboBox_search.currentIndexChanged.connect(ui.SearchBy)
    ui.lineEdit_searchby.textEdited.connect(ui.SearchBy)
    # tab 2
    ui.Button_Refresh.clicked.connect(ui.FillTableTab2)
    # tab 3
    ui.Button_process.clicked.connect(ui.ButtonProcess)
    ui.comboBox_sort.currentIndexChanged.connect(ui.FillTableTab2)
    # tab 4
    ui.Button_process_2.clicked.connect(ui.ButtonProcess2)
    # endregion

    MainWindow.show()
    sys.exit(app.exec_())
