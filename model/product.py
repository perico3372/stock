#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')


from model.supplier import Supplier
from model.brand import Brand
from model.category import Category

class Product(object):
    def __init__(self):

        self.__productId = 0
        self.__ProductName = ""
        self.__ProductQuantity = 0
        self.__ProductMinimumQuantity = 0
        self.__ProductDescription = ""
        self.__genre = ""
        self.__category = Category()
        self.__supplier = Supplier()
        self.__brand = Brand()
        self.__status = 0
        self.__purchasePrice = 0,00
        self.__salesPrice = 0,00

    def setProductId(self, productId):
        self.__productId = productId

    def getProductId(self):
        return self.__productId

    def setProductName(self, name):
        self.__ProductName = name

    def getProductName(self):
        return self.__ProductName

    def setProductQuantity(self, quantity):
        self.__ProductQuantity = quantity

    def getProductQuantity(self):
        return self.__ProductQuantity

    def setProductMinimumQuantity(self, minimumQuantity):
        self.__ProductMinimumQuantity = minimumQuantity

    def getProductMinimumQuantity(self):
        return self.__ProductMinimumQuantity

    def setProductDescription(self, description):
        self.__ProductDescription = description

    def getProductDescription(self):
        return self.__ProductDescription

    def setProductGenre(self, genre):
        self.__genre = genre

    def getProductGenre(self):
        return self.__genre

    def setProductCategory(self, category):
        self.__category = category

    def getProductCategory(self):
        return self.__category

    def setProductSupplier(self, supplier):
        self.__supplier = supplier

    def getProductSupplier(self):
        return self.__supplier

    def setProductBrand(self, brand):
        self.__brand = brand

    def getProductBrand(self):
        return self.__brand

    def setProductStatus(self, status):
        self.__status = status

    def getProductStatus(self):
        return self.__status

    def setPurchasePrice(self, purchasePrice):
        self.__purchasePrice = purchasePrice

    def getPurchasePrice(self):
        return self.__purchasePrice

    def setProductSalesPrice(self, salesPrice):
        self.__salesPrice = salesPrice

    def getProductSalesPrice(self):
        return self.__salesPrice