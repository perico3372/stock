#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:38:32 2023

@author: pablo
"""

import sys
sys.path.append('..')

from model.table import TableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QCompleter, QLineEdit, QComboBox
from connection.productConnection import ProductConnection
from brandWindow import BrandWindow
from categoryWindow import CategoryWindow
from model.supplier import Supplier
from model.product import Product
from model.category import Category
from model.brand import Brand
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel
from PyQt5 import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication

from PyQt5.QtGui import QStandardItemModel

class ProductsTab():

    def __init__(self, mainWindows):
        self.mainWindows = mainWindows
        self.product = Product()
        self.supplier = Supplier()
        self.brand = Brand()
        self.category = Category()
        self.estado = ""
        self.productConnection = ProductConnection()
        self.supplierListing = QComboBox()
        self.brandlisting = QComboBox()
        self.categoryListing = QComboBox()
        self.configInit()

    def configInit(self):
        # Configurando botones
        self.mainWindows.btnAddProductsTab.clicked.connect(self.enableButtonAddProductsTab)
        self.mainWindows.btnSaveProductsTab.clicked.connect(self.enableButtonSaveProductsTab)

        # Crear instancias de QComboBox
        self.comboBoxSupplier = QComboBox(self.mainWindows)
        self.comboBoxCategory = QComboBox(self.mainWindows)
        self.comboBoxBrand = QComboBox(self.mainWindows)

        # Conectar señales a métodos
        self.comboBoxSupplier.editTextChanged.connect(self.changeComboBoxSuppliers)
        self.comboBoxCategory.editTextChanged.connect(self.changeComboBoxCategories)
        self.comboBoxBrand.editTextChanged.connect(self.changeComboBoxBrands)

        # Obtener datos y agregar al QComboBox
        supplierList = [(name, supplierId) for name, supplierId in self.productConnection.suppliersListing()]
        categoryList = [(name, categoryId) for name, categoryId in self.productConnection.categoriesListing()]
        brandList = [(name, brandId) for name, brandId in self.productConnection.brandsListing()]

        # Limpiar ComboBox antes de agregar elementos
        self.comboBoxSupplier.clear()
        self.comboBoxCategory.clear()
        self.comboBoxBrand.clear()

        # Agregar elementos a ComboBox
        for supplierId, name in supplierList:
            self.comboBoxSupplier.addItem(name, userData=supplierId)

        for categoryId, name in categoryList:
            self.comboBoxCategory.addItem(name, userData=categoryId)

        for brandId, name in brandList:
            self.comboBoxBrand.addItem(name, userData=brandId)

        self.mainWindows.txtFilterProductProductsTab.setFocus(True)

    def finish(self):
        self.mainWindows.btnAddProductsTab.disconnect()
        self.mainWindows.btnSaveProductsTab.disconnect()
        self.mainWindows.btnUpdateProductsTab.disconnect()
        self.mainWindows.btnDeleteProductsTab.disconnect()
        self.mainWindows.btnCategoryProductsTab.disconnect()
        self.mainWindows.btnBrandProductsTab.disconnect()
        self.mainWindows.tvProductProductsTab.disconnect()

    def search(self):
        if self.mainWindows.txtFilterProductProductsTab.hasFocus() is True:
            self.loadTable()

    def enableButtonAddProductsTab(self):
        self.estado = 'AGREGAR'
        self.validateButtons(button='AGREGAR')

    def enableButtonSaveProductsTab(self):
        validate = self.validate()

        if validate != "":
            print(validate)
            alert = QDialog()
            QMessageBox.information(alert, "ERROR", validate)
        else:
            self.product.setProductName(str(self.mainWindows.txtProductDescriptionProductsTab.toPlainText()))
            self.product.setProductQuantity(int(self.mainWindows.sbQuantityProductsTab.value()))
            self.product.setProductMinimumQuantity(int(self.mainWindows.sbMinimumQuantityProductsTab.value()))
            if self.mainWindows.cbProductStatusProductsTab.currentText() == "ACTIVO":
                self.product.setProductStatus(1)
            else:
                self.product.setProductStatus(0)

            if self.mainWindows.rbFemaleProductsTab.isChecked() is True:
                self.product.setProductGenre("F")
            elif self.mainWindows.rbMaleProductsTab.isChecked() is True:
                self.product.setProductGenre("M")
            else:
                self.product.setProductGenre("I")

            self.product.setProductName(str(self.mainWindows.txtProductNameProductsTab.text()))
            self.product.setPurchasePrice(float(self.mainWindows.txtPurchasePriceProductsTab.text()))
            self.product.setProductSalesPrice(float(self.mainWindows.txtSalesPriceProductsTab.text()))

            self.category.setCategoryId(str(self.comboBoxCategory.currentIndexChanged.connect(self.changeComboBoxCategories)))
            # self.product.setProductCategory(self.category)

            self.supplier.setPersonId(str(self.comboBoxSupplier.currentIndexChanged.connect(self.changeComboBoxSuppliers)))
            # # self.product.setProveedor(self.supplier)

            self.brand.setBrandId(str(self.comboBoxBrand.currentIndexChanged.connect(self.changeComboBoxBrands)))
            # # self.product.setBrandName(self.brand)

            if self.estado == 'AGREGAR':
                self.addProduct()
            elif self.estado == 'MODIFICAR':
                self.updateProduct()

            self.validateButtons('GUARDAR')

    def validateButtons(self, button):
        if button == 'AGREGAR':
            self.mainWindows.wDatosProducto.setEnabled(True)
            self.mainWindows.btnDeleteProductsTab.setEnabled(True)
            self.mainWindows.btnDeleteProductsTab.setText('CANCELAR')
            self.mainWindows.btnSaveProductsTab.setEnabled(True)
            self.mainWindows.btnUpdateProductsTab.setEnabled(False)
            self.mainWindows.btnAddProductsTab.setEnabled(False)
            self.mainWindows.tvProductProductsTab.setEnabled(False)
            self.cleanFields()

        elif button == 'GUARDAR':
            self.mainWindows.btnUpdateProductsTab.setEnabled(False)
            self.mainWindows.btnAddProductsTab.setEnabled(True)
            self.mainWindows.btnSaveProductsTab.setEnabled(False)
            self.mainWindows.btnDeleteProductsTab.setText('BORRAR')
            self.mainWindows.btnDeleteProductsTab.setEnabled(False)
            self.mainWindows.tvProductProductsTab.setEnabled(True)
            self.mainWindows.wDatosProducto.setEnabled(False)
            self.cleanFields()

        elif button == 'MODIFICAR':
            self.mainWindows.btnUpdateProductsTab.setEnabled(False)
            self.mainWindows.btnAddProductsTab.setEnabled(False)
            self.mainWindows.btnSaveProductsTab.setEnabled(True)
            self.mainWindows.btnDeleteProductsTab.setText('CANCELAR')
            self.mainWindows.btnDeleteProductsTab.setEnabled(True)
            self.mainWindows.tvProductProductsTab.setEnabled(False)
            self.mainWindows.wDatosProducto.setEnabled(True)

        elif button == 'BORRAR':
            self.mainWindows.btnUpdateProductsTab.setEnabled(False)
            self.mainWindows.btnAddProductsTab.setEnabled(True)
            self.mainWindows.btnSaveProductsTab.setEnabled(False)
            self.mainWindows.btnDeleteProductsTab.setText('BORRAR')
            self.mainWindows.btnDeleteProductsTab.setEnabled(False)
            self.mainWindows.tvProductProductsTab.setEnabled(True)
            self.mainWindows.wDatosProducto.setEnabled(False)
            self.cleanFields()

    def addProduct(self):
        self.productConnection.addProduct(product=self.product)
        # self.loadTable()

    def cleanFields(self):
        self.mainWindows.txtProductNameProductsTab.setText('')
        self.mainWindows.txtPurchasePriceProductsTab.setText('')
        self.mainWindows.txtSalesPriceProductsTab.setText('')
        self.mainWindows.sbQuantityProductsTab.setValue(0)
        self.mainWindows.sbMinimumQuantityProductsTab.setValue(0)
        self.mainWindows.cbSupplierProductsTab.clear()
        self.mainWindows.txtProductDescriptionProductsTab.setText('')
        self.mainWindows.cbCategoryProductsTab.clear()
        self.mainWindows.cbBrandProductsTab.clear()
        self.mainWindows.txtFilterProductProductsTab.setText('')
        self.mainWindows.tvProductProductsTab.setModel(None)

        self.mainWindows.txtFilterProductProductsTab.setFocus(True)

    def validate(self):
        mensaje = ''
        if self.mainWindows.txtProductNameProductsTab.text() == '':
            mensaje = "Falta ingresar Nombre"
        elif self.mainWindows.txtPurchasePriceProductsTab.text() == '':
            mensaje = "Falta ingresar Precio de Compra"
        elif self.mainWindows.txtSalesPriceProductsTab.text() == '':
            mensaje = "Falta ingresar Precio de Venta"
        # elif self.supplierCompleter.currentCompletion() =='':
        #   mensaje= "Falta ingresar un Proveedor"
        # elif self.brandCompleter.currentCompletion() == '':
        #  mensaje = "Falta seleccionar la marca"
        # elif self.categoryCompleter.currentCompletion() == '':
        #   mensaje = 'Falta seleccionar el rubro'

        return mensaje

    def changeComboBoxSuppliers(self, text):
        # Obtener el proveedor ingresado o seleccionado
        selectedSupplier = text
        # Realizar el resto de la lógica según tus necesidades

    def changeComboBoxCategories(self, text):
        # Obtener la categoría ingresada o seleccionada
        selectedCategory = text
        # Realizar el resto de la lógica según tus necesidades

    def changeComboBoxBrands(self, text):
        # Obtener la marca ingresada o seleccionada
        selectedBrand = text
        # Realizar el resto de la lógica según tus necesidades

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ProductsTab()
    mainWin.show()
    sys.exit(app.exec_())
