# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

class Address:
    def __init__(self):
        self.__addressId = 0
        self.__addressStreet = ""
        self.__addressNumber = 0
        self.__addressFloor = 0
        self.__addressDpto = ""

    def setAddressId(self, addressId):
        self.__addressId = addressId

    def getAddressId(self):
        return self.__addressId

    def setAddressStreet(self, street):
        self.__addressStreet = street

    def getAddressStreet(self):
        return self.__addressStreet

    def setAddressNumber(self, number):
        self.__addressNumber = number

    def getAddressNumber(self):
        return self.__addressNumber

    def setAddressFloor(self, floor):
        self.__addressFloor = floor

    def getAddressFloor(self):
        return self.__addressFloor

    def setAddressDpto(self, dpto):
        self.__addressDpto = dpto

    def getAddressDpto(self):
        return self.__addressDpto





# import sys
# sys.path.append('..')

# class Address:
#     def __init__(self):
#         self.__addressId = 0
#         self.__addressStreet = ""
#         self.__addressNumber = 0
#         self.__addressFloor = 0
#         self.__addressDpto = ""

#     def setAddressId(self, addressId):
#         self.__addressId = addressId

#     def getAddressId(self):
#         return self.__addressId

#     def setAddressStreet(self, address):
#         self.__addressStreet = address

#     def getAddressStreet(self):
#         return self.__addressStreet

#     def setAddressNumber(self, number):
#         self.__addressNumber = number

#     def getAddressNumber(self):
#         if self.__addressNumber != 0:
#             return self.__addressNumber
#         else:
#             return None

#     def setAddressFloor(self, floor):
#         self.__addressFloor = floor

#     def getAddressFloor(self):
#         if self.__addressFloor != 0:
#             return self.__addressFloor
#         else:
#             return None

#     def setAddressDpto(self, dpto):
#         self.__addressDpto = dpto

#     def getAddressDpto(self):
#         if self.__addressDpto != "":
#             return self.__addressDpto
#         else:
#             return None
