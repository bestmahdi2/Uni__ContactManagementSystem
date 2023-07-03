# import pickle
#
# Database = [{"first name": 'ali', "last name": 'cad', "email": 'alibad@gamil.com', "phone": '0910'},
#                  {"first name": 'mahdi', "last name": 'bad', "email": 'mahdi@gamil.com', "phone": '0912'}]
#
# with open('listfile.txt', 'wb') as filehandle:
#     # store the data as binary data stream
#     pickle.dump(Database, filehandle)
#
#
# with open('listfile.txt', 'rb') as filehandle:
#     # read the data as binary data stream
#     placesList = pickle.load(filehandle)
#
#     print(placesList, type(placesList))