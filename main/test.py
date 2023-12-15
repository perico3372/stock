#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:38:20 2023

@author: pablo
"""

import sys

#from PyQt5.QtWidgets import QAction, QMainWindow
from PyQt5 import uic

#from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication 

from PyQt5.QtWidgets import QApplication 
import pymysql
from PyQt5 import uic


class DatabaseConnection(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.dbHost ='localhost'
        self.dbPort = 3306
        self.dbUser = 'root'
        self.dbPassword = 'patacon'
        self.dbName ='test'
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
        
class Supplier(object):
    def __init__(self):
        
        self.__supplierId = 0
        self.__supplierName = ""

    def setSupplierId(self, supplierId):
        self.__supplierId = supplierId

    def getSupplierId(self):
        return self.__supplierId

    def setSupplierName(self, supplierName):
        self.__supplierName = supplierName

    def getSupplierName(self):
        return self.__supplierName

class Product(object):
    def __init__(self):

        self.__productId = 0
        self.__ProductName = ""

    def setProductId(self, productId):
        self.__productId = productId

    def getProductId(self):
        return self.__productId

    def setProductName(self, name):
        self.__ProductName = name

    def getProductName(self):
        return self.__ProductName

class Connection(object):
   
    databaseConnection = DatabaseConnection()
    def suppliersListing(self):
        query = "SELECT supplierId, supplierName FROM suppliers"
        
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        auxListSupplier = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        
        # Crear una lista de tuplas (ID, nombre) para los proveedores
        suppliersList = [(str(supplier[1]), supplier[0]) for supplier in auxListSupplier]
        
        # Agregar un elemento vacío al principio de la lista
        suppliersList.insert(0, (0, ''))
        
        return suppliersList
    
    def insert_supplier(self, supplier_name):
        query = f"INSERT INTO suppliers (supplierName) VALUES ('{supplier_name}')"
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()
    def insert_product(self, product_name, supplier_id):
            # Asegúrate de que supplier_id sea un entero
            supplier_id = int(supplier_id)
    
            query = "INSERT INTO products (nameProduct, suppliers_supplierId) VALUES (%s, %s)"
            values = (product_name, supplier_id)
            self.databaseConnection.openConnection()
            self.databaseConnection.cursor.execute(query, values)
            self.databaseConnection.db.commit()
            self.databaseConnection.closeConnection()

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit

class MainWindow:

    def __init__(self):
        self.mainWindow = uic.loadUi('../view/test.ui')
        self.comboBoxSupplier = self.mainWindow.comboBoxSupplier
        self.populate_supplier_combobox()

        add_product_button = self.mainWindow.pushButtonAddProduct
        add_product_button.clicked.connect(self.handle_add_product)

        self.mainWindow.show()

    def populate_supplier_combobox(self):
        connection = Connection()
        suppliers_list = connection.suppliersListing()
        self.comboBoxSupplier.clear()
        for supplier_name, supplier_id in suppliers_list:
            self.comboBoxSupplier.addItem(str(supplier_name), supplier_id)

    def handle_add_product(self):
        product = Product()
        product.setProductName(self.get_product())

        supplier = Supplier()
        supplier.setSupplierId(self.get_suppliers())

        if product.getProductName() and supplier.getSupplierId() is not None:
            connection = Connection()
            connection.insert_product(product.getProductName(), supplier.getSupplierId())
            print("Producto agregado correctamente.")

    def get_product(self):
        return self.mainWindow.lineEditProduct.text()

    def get_suppliers(self):
        selected_supplier_index = self.comboBoxSupplier.currentIndex()
        return self.comboBoxSupplier.itemData(selected_supplier_index)

if __name__ == "__main__":
    # Crear una instancia de la clase ConexionProducto
    connection = Connection()
    print(connection.suppliersListing())
 
app = QApplication(sys.argv)
init = MainWindow()
sys.exit(app.exec_())

