#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.person import Person

class Supplier(Person):
    def __init__(self):
        Person.__init__(self)
        self.__supplierId = 0
        self.__supplierName = ""
        self.__supplierWeb = ""
        #self.__supplierStatus = 0

    def setSupplierId(self, supplierId):
        self.__supplierId = supplierId

    def getSupplierId(self):
        return self.__supplierId

    def setSupplierName(self, supplierName):
        self.__supplierName = supplierName

    def getSupplierName(self):
        return self.__supplierName

    def setSupplierWeb(self, supplierWeb):
        self.__supplierWeb = supplierWeb

    def getSupplierWeb(self):
        return self.__supplierWeb

    # def setSupplierStatus(self, supplierStatus):
    #     self.__supplierStatus = supplierStatus

    # def getSupplierStatus(self):
    #     return self.__supplierStatus


