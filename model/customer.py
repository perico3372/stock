#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from model.person import Person

class Customer(Person):

    def __init__(self):
        Person.__init__(self)
        
        self.__customerId = 0
        self.__customerStatus = 0

    def setCustomerId(self, customerId):
        self.__customerId = customerId

    def getCustomerId(self):
        return self.__CustomerId

    def setCustomerStatus(self, status):
        self.__customerStatus = status

    def getCustomerStatus(self):
        return self.__customerStatus