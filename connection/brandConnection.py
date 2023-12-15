#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.brand import Brand

class BrandConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.brand = Brand() 

    def brandsListing(self, textFilter):
        query = "SELECT brandId, brandDescription FROM brands WHERE brandDescription LIKE %s"
        parameter = textFilter + '%'
        self.databaseConnection.openConnecttion() 
        self.databaseConnection.cursor.execute(query, parameter)
        brandList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnecttion()
        return brandList

    def deleteBrands(self, brand):
        query = "DELETE FROM brands WHERE brandId = %s"
        values = brand.getBrandId()
        self.databaseConnection.openConnecttion()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnecttion()

    def UpdateBrands(self, brand):
        query = "UPDATE brands SET brandDescription = %s WHERE brandId = %s"
        values = (brand.getBrandName(), brand.getBrandId())
        self.databaseConnection.openConnecttion()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnecttion()

    def AddBrands(self, brand):
        query = "INSERT INTO brands (brandDescription) VALUES (%s)"
        values = brand.getBrandName()
        self.databaseConnection.openConnecttion()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnecttion()
