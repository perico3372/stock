#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 10:09:52 2023

@author: pablo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 08:53:42 2023

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
        query = f"INSERT INTO products (nameProduct, suppliers_supplierId) VALUES ('{product_name}', {supplier_id})"
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLineEdit

class MainWindow:

    
    def __init__(self):
        self.mainWindow = uic.loadUi('../view/test.ui')
        self.comboBoxSupplier = self.mainWindow.comboBoxSupplier  # Obtener referencia al comboBox
        self.lineEditProduct = self.mainWindow.lineEditProduct
        self.pushButtonAddProduct = self.mainWindow.pushButtonAddProduct
        self.pushButtonEnableEdit = self.mainWindow.pushButtonEnableEdit

        # Conectar la señal del comboBox a una función para manejar eventos
        self.comboBoxSupplier.currentIndexChanged.connect(self.handle_supplier_selection_change)

        # Conectar el botón para agregar productos a la función correspondiente
        self.pushButtonAddProduct.clicked.connect(self.handle_add_product)

        # Conectar el botón de habilitar/deshabilitar a la función correspondiente
        self.pushButtonEnableEdit.clicked.connect(self.handle_enable_edit)

        # Deshabilitar el line edit y el combo box inicialmente
        self.lineEditProduct.setEnabled(False)
        self.comboBoxSupplier.setEnabled(False)

        self.mainWindow.show()
    
    def handle_enable_edit(self):
            # Cambiar el estado de habilitado/deshabilitado de los widgets
            enable_edit = not self.lineEditProduct.isEnabled()
            self.lineEditProduct.setEnabled(enable_edit)
            self.comboBoxSupplier.setEnabled(enable_edit)
            self.pushButtonAddProduct.setEnabled(enable_edit)
            self.pushButtonEnableEdit.setText("Deshabilitar Edición" if enable_edit else "Habilitar Edición")


    def populate_supplier_combobox(self):
        # Crear una instancia de la clase Connection
        connection = Connection()

        # Obtener la lista de proveedores
        suppliers_list = connection.suppliersListing()

        # Limpiar el comboBox antes de agregar elementos
        self.comboBoxSupplier.clear()

        # Agregar elementos al comboBox
        for supplier_name, supplier_id in suppliers_list:
            self.comboBoxSupplier.addItem(str(supplier_name), supplier_id)  # Convertir a cadena

  
    def handle_supplier_selection_change(self):
    # Manejar el cambio de selección en el comboBox
        selected_supplier_index = self.comboBoxSupplier.currentIndex()
        selected_supplier_id = self.comboBoxSupplier.itemData(selected_supplier_index, role=Qt.UserRole)
        print(f"Proveedor seleccionado: {selected_supplier_id}")

    
    def handle_supplier_selection_change(self):
        # Manejar el cambio de selección en el comboBox
        selected_supplier_index = self.comboBoxSupplier.currentIndex()
        selected_supplier_id = self.comboBoxSupplier.itemData(selected_supplier_index)
        print(f"Proveedor seleccionado: {selected_supplier_id}")

    def handle_add_product(self):
        # Obtener el nombre del producto y el ID del proveedor
        product_name = self.mainWindow.lineEditProduct.text()
        selected_supplier_index = self.comboBoxSupplier.currentIndex()
        supplier_id = self.comboBoxSupplier.itemData(selected_supplier_index)

        # Verificar que el nombre del producto y el ID del proveedor no estén vacíos
        if product_name and supplier_id is not None:
            connection = Connection()
            connection.insert_product(product_name, supplier_id)
            print("Producto agregado correctamente.")
# if __name__ == "__main__":
#     # Crear una instancia de la clase ConexionProducto
#     connection = Connection()
#     print(connection.suppliersListing())
app = QApplication(sys.argv)
init = MainWindow()
sys.exit(app.exec_())
