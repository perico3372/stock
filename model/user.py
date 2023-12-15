#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.person import Person
import hashlib

class User(Person):

    def __init__(self):
        Person.__init__(self)
        self.__userId = 0
        self.__userName = ""
        self.__userPasswd = ""
        self.__userType = ""
        self.__userPersonName = Person() 

    def setUserPerson(self, PersonName):
        self.__userPersonName = PersonName

    def getUserPerson(self):
        return self.__userPersonName

    def setUserName(self, user):
        self.__userName = user

    def getUserName(self):
        return self.__userName

    def setUserPasswd(self, passwd):
        #auxPasswd = hashlib.md5(passwd).hexdigest()
        self.__userPasswd = passwd

    def getUserPasswd(self):
        return self.__userPasswd

    def setUserType(self, userType):
        self.__userType = userType

    def getUserType(self):
        return self.__userType

    def setUserId(self, userId):
        self.__userId = userId

    def getUserId(self):
        return self.__userId