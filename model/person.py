#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from model.address import Address

class Person(Address):
    def __init__(self):
        self.__personId = 0
        self.__namePerson = ""
        self.__emailPerson = ""
        self.__personStatus = 0
        #self.__addressPerson = Address()

    def setPersonId(self, personId):
        self.__personId = personId

    def getPersonId(self):
        return self.__personId

    def setPersonName(self, name):
        self.__namePerson = name

    def getPersonName(self):
        return self.__namePerson

    def setPersonEmail(self, email):
        self.__emailPerson = email

    def getPersonEmail(self):
        return self.__emailPerson

    # def setPersonAddress(self, address):
    #     if isinstance(address, Address):
    #         self.__addressPerson = address
    #     else:
    #         raise ValueError("Invalid address type. Must be an instance of Address.")

    # def getPersonAddress(self):
    #     return self.__addressPerson

    def setPersonStatus(self, personStatus):
        self.__personStatus = personStatus

    def getPersonStatus(self):
        return self.__personStatus
