from os import makedirs
from typing import Union


class CMSDictProcess:
    def CreateContact(self, dicts: dict, info: list) -> Union[dict, bool]:
        """This function gets a dictionary and a list of data,
            adds that information to dictionary if no duplicates were found,
            then returns the dictionary or returns duplicated data trigger"""

        if dicts.keys():
            last_index = max([int(i) for i in dicts.keys()])
        else:
            last_index = 0

        if isinstance(self.DuplicateContact(dicts, info), bool):
            return True

        else:
            dicts[str(last_index + 1)] = {"firstName": info[0],
                                          "lastName": info[1],
                                          "phone": info[2],
                                          "email": info[3],
                                          "extras": info[4]}

            return dicts

    def DeleteContact(self, dicts: dict, index: str) -> dict:
        """This function gets a dictionary and a string key,
           deletes that key from dictionary,
           then returns the dictionary"""

        try:
            del dicts[index]
        except KeyError:
            pass

        dicts = self.SortContact(dicts, mode="delete")
        return dicts

    def EditContact(self, dicts: dict, index: str, info: list) -> Union[dict, bool]:
        """This function gets a dictionary, a string key and a list of information,
           it changes dictionary values by the list,
           then if doesn't make a duplicate, returns the dictionary else returns duplicated data trigger"""

        if isinstance(self.DuplicateContact(dicts, info), bool):
            return True

        else:
            changed = {"firstName": info[0],
                       "lastName": info[1],
                       "phone": info[2],
                       "email": info[3],
                       "extras": info[4]}
            try:
                dicts[index] = changed
            except KeyError:
                pass

            return dicts

    @staticmethod
    def FindContact(dicts: dict, mode: str, key: str) -> list:
        """This function gets a dictionary, a string key and mode,
           it creates a list and appends data which are same with the key,
           then returns the list"""

        keeper = []
        for i in list(dicts.items()):
            if key in i[1][mode].lower():
                keeper.append(i[0])

        return keeper

    @staticmethod
    def SortContact(dicts: dict, mode: str) -> dict:
        """This function gets dictionary and a string key,
           it sorts dictionary with this key,
           then returns the dictionary"""

        if mode == "delete":
            sort = {k: v for k, v in list(dicts.items())}
        else:
            sort = {k: v for k, v in sorted(dicts.items(), key=lambda item: item[1][mode])}

        dicts, x = {}, 0
        while x < len(list(sort.values())):
            dicts[str(x + 1)] = list(sort.values())[x]
            x += 1

        return dicts

    @staticmethod
    def DuplicateContact(dicts: dict, info: list) -> bool:
        """This function gets a dictionary and a list,
           it finds duplicated list data in dictionary,
           then if it finds anything returns the list"""

        if dicts:
            keys = list(list(dicts.values())[0].keys())
            for i in dicts.keys():
                x = 0
                cache = []
                for mode in keys:
                    if dicts[i][mode] == info[x]:
                        cache.append(mode)
                    x += 1
                if len(cache) == len(info):
                    return True


class CMSTextProcess:
    @staticmethod
    def FileToDict(address: str) -> Union[dict, bool]:
        """This function gets a string address of a file,
           it opens the file and save file data to dictionary,
           then if it was successful returns the dictionary else returns error in writing file trigger"""

        dicts = {}
        try:
            with open(address, "r", encoding="utf-8") as file:
                junk_removed_ = [i for i in file.readlines() if i.replace(" ", "").replace("\n", "")]
                junks = ["Name = ", "Lastname = ", "PhoneNumber = ", "Email = ", "Extras = ", "====== ", "======"]

                for i in junks:
                    x = 0
                    while x < len(junk_removed_):
                        junk_removed_[x] = junk_removed_[x].replace(i, "").replace("\n", "")
                        x += 1

                junk_removed = []
                for i in junk_removed_:
                    if i and i == "战":
                        junk_removed.append("")
                    elif i:
                        junk_removed.append(i)

                for i in range(0, len(junk_removed), 6):
                    dicts[junk_removed[i]] = {"firstName": junk_removed[i + 1],
                                              "lastName": junk_removed[i + 2],
                                              "phone": junk_removed[i + 3],
                                              "email": junk_removed[i + 4],
                                              "extras": junk_removed[i + 5]}
        except IndexError:
            return False
        except FileNotFoundError:
            makedirs(address[:address.rfind("\\")], exist_ok=True)
            try:
                file = open(address, "w", encoding="utf-8")
                file.close()
            except FileNotFoundError:
                return False

        if dicts and "1" not in list(dicts.keys()):
            return False
        return dicts

    @staticmethod
    def DictToFile(address: str, dicts: dict) -> None:
        """This function gets a string address and a dictionary,
           it writes dictionary data into file"""

        if dicts:
            to_print = []
            for i in dicts.keys():
                info = dicts[i]

                keeper = [f"====== {i}",
                          f"Name = {info['firstName']}",
                          f"Lastname = {info['lastName'] if info['lastName'] else '战'}",
                          f"PhoneNumber = {info['phone'] if info['phone'] else '战'}",
                          f"Email = {info['email'] if info['email'] else '战'}",
                          f"Extras = {info['extras'] if info['extras'] else '战'}",
                          "======"]

                to_print.append("\n".join(keeper))

            with open(address, "w", encoding="utf-8") as file:
                file.write("\n\n".join(to_print))

        else:
            makedirs(address[:address.rfind("\\")], exist_ok=True)
            file = open(address, "w", encoding="utf-8")
            file.close()

    @staticmethod
    def DictToJsonXml(dicts: dict) -> None:
        """This function gets a dictionary,
           it creates a file in whatever type user wants in json or xml format"""

        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_name = filedialog.asksaveasfilename(title="Save as...", defaultextension="json",
                                                 initialfile="database1.json", initialdir="./",
                                                 filetypes=(("JSON", "*.json"), ("XML", "*.xml"), ("All Files", "*.*")))

        if file_name:
            if file_name.lower().endswith(".json"):
                import json
                with open(file_name, 'w') as fp:
                    json.dump(dicts, fp)

            elif file_name.lower().endswith(".xml"):
                keeper = ["<Contacts>"]
                for i in list(dicts.keys()):
                    temp = ["\t<Contact>", f"\t\t<id>{i}</id>"]
                    for j in list(dicts[i].keys()):
                        temp.append(f'\t\t<{j}>{dicts[i][j]}</{j}>')
                    temp.append("\t</Contact>")

                    keeper.append("\n".join(temp))

                keeper.append("</Contacts>")

                with open(file_name, 'w') as fp:
                    fp.write("\n".join(keeper))

    @staticmethod
    def EmailVerification(email: str) -> bool:
        """This function gets a string email address,
           it defines if the address is valid or not,
           then returns the result"""

        import re
        regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if re.search(regex, email):
            return True
        else:
            return False

    @staticmethod
    def TextCrawler(text: str) -> list:
        """This function gets a string text,
           it creates a list, finds and appends the names and phone numbers,
           then returns the list"""

        import re
        name = re.findall('[@]+([A-Za-z]+)', text)
        phones = re.findall('[#]+([0-9]+)', text)

        return [name, phones]

    @staticmethod
    def WebScraping() -> Union[list, bool]:
        """This function extracts data from a web page,
        it returns data needed or returns False if there is no connection to internet"""

        url = "https://www.fakenamegenerator.com/"
        try:

            from bs4 import BeautifulSoup
            from lxml import etree
            import requests

            HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                        'Accept-Language': 'en-US, en;q=0.5'})

            webpage = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")
            dom = etree.HTML(str(soup))

            name = dom.xpath('//*[@id="details"]/div[2]/div[2]/div/div[1]/h3')[0].text
            LastName = name.split()[-1]
            FirstName = name.replace(f' {LastName}', "")

            contryCode = dom.xpath('//*[@id="details"]/div[2]/div[2]/div/div[2]/dl[5]/dd')[0].text
            phone = f'+{contryCode} ' + dom.xpath('//*[@id="details"]/div[2]/div[2]/div/div[2]/dl[4]/dd/text()')[0]
            email = dom.xpath('//*[@id="details"]/div[2]/div[2]/div/div[2]/dl[9]/dd/text()')[0]

            return [FirstName, LastName, phone, email.replace(" ", "")]

        except:
            return False


if __name__ == '__main__':
    input("Try to open 'main.py'")
