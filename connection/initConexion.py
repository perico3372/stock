#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from connection.productConnection import ProductConnection
from connection.supplierConnection import SupplierConnection
from connection.customerConnection import CustomerConnection
from connection.userConnection import UserConnection
from connection.brandConnection import BrandConnection
from connection.categoryConnection import CategoryConnection

class ControllerConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.customerConnection = CustomerConnection(self.databaseConnection)

    def getCategoryConnection(self):
        self.__categoryConnection = CategoryConnection(self.databaseConnection)
        return self.__categoryConnection

    def getBrandConnection(self):
        self.__brandConnection = BrandConnection(self.__connection)
        return  self.__brandConnection

    def getUserConnection(self):
        self.__userConnection = UserConnection(self.__connection)
        return self.__userConnection

    def getCustomerConnection(self):
        return self.connectionCustomer

    def getSupplierConnection(self):
        self.__connectionSupplier = ConnectionSupplier(self.__connection)
        return self.__connectionSupplier

    def getProductConnection(self):
        self.__connectionProduct = ConnectionProduct(self.__connection)
        return self.__connectionProduct

