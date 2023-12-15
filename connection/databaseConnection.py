#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

class DatabaseConnection(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.dbHost ='localhost'
        self.dbPort = 3306
        self.dbUser = 'root'
        self.dbPassword = 'patacon'
        self.dbName ='DB'
        self.db = None  # Initialize the database connection attribute
        
    def connection(self):
        self.db = pymysql.connect(host=self.dbHost, user=self.dbUser,
                                  passwd=self.dbPassword, db=self.dbName)
        return self.db  # Return the database connection object

    def openCursor(self):
        self.cursor = self.db.cursor()

    def closeCursor(self):
        self.cursor.close()
        
    def close_connection(self):
        self.db.close()

    def openConnection(self):
        if (self.dbHost and self.dbName and self.dbPassword and self.dbPort and self.dbUser):
            self.connection()
            self.openCursor()
    
    def closeConnection(self):
        self.closeCursor()
        self.close_connection()  