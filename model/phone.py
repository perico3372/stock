
import sys
sys.path.append('..')

from model.person import Person

class Phone(object):

    def __init__(self):
        self.__phoneId = 0
        self.__phoneType = ""
        self.__phoneNumber = 0
        self.__PersonId = 0

    def setPhoneId(self, phoneId):
        self.__phoneId = phoneId

    def getPhoneId(self):
        return self.__idPhone

    def setPhoneType(self, type):
        self.__type = type

    def getPhoneType(self):
        return self.__type

    def setPhoneNumber(self, phone):
        self.__phoneNumber = phone

    def getPhoneNumber(self):
        return self.__phoneNumber

    def setPersonId(self, personId):
        self.__personId = personId

    def getPersonId(self):
        return self.__personId