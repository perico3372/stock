#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.category import Category

class CategoryConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.category = Category()

    def selectCategory(self, filterText):
        query = "SELECT categoryId, categoryDescription FROM categories WHERE categoryDescription LIKE %s"
        parametro = filterText + '%'
        value = parametro
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, value)
        categoryList = self.databaseConnection.cursor.fetchall()

        return categoryList
        self.databaseConnection.closeConnection()


    def deleteCategory(self, category):
        query = "DELETE FROM categories WHERE categoryId = %s"
        values = category.getCategoryId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()


    def connectionUpdateCategory(self, category):
        query = "UPDATE categories SET categoryDescription = %s WHERE categoryId = %s"
        values = (category.getCategoryName(), category.getCategoryId())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()


    def connectionCategoryAdd(self, category):
        query = "INSERT INTO categories (categoryDescription) VALUES (%s)"
        values = category.getRubro()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()
