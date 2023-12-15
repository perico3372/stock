#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from PyQt5.QtWidgets import QMessageBox, QDialog,QApplication



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
        self.comboBoxSupplier = QComboBox(self)
        self.comboBoxSupplier.setEditable(True)

        self.comboBoxCategory = QComboBox(self)
        self.comboBoxCategory.setEditable(True)

        self.comboBoxBrand = QComboBox(self)
        self.comboBoxBrand.setEditable(True)

        # Inicializar ComboBox
        self.changeComboBoxSuppliers()
        self.changeComboBoxCategories()
        self.changeComboBoxBrands()

        # Conectar señales a métodos
        self.comboBoxSupplier.currentIndexChanged.connect(self.changeComboBoxSuppliers)
        self.comboBoxCategory.currentIndexChanged.connect(self.changeComboBoxCategories)
        self.comboBoxBrand.currentIndexChanged.connect(self.changeComboBoxBrands)

        # Obtener datos y agregar al QComboBox
        self.comboBoxSupplier.addItems([name for name, _ in self.productConnection.suppliersListing()])
        self.comboBoxCategory.addItems([name for name, _ in self.productConnection.categoriesListing()])
        self.comboBoxBrand.addItems([name for name, _ in self.productConnection.brandsListing()])

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


    def changeComboBoxSuppliers(self):
        # Obtener el proveedor seleccionado
        selectedSupplier = self.comboBoxSupplier.currentText()

        # Limpiar y agregar elementos al ComboBox
        self.comboBoxSupplier.clear()
        self.comboBoxSupplier.addItems([name for name, _ in self.productConnection.suppliersListing()])

    def changeComboBoxCategories(self):
        # Obtener la categoría seleccionada
        selectedCategory = self.comboBoxCategory.currentText()

        # Limpiar y agregar elementos al ComboBox
        self.comboBoxCategory.clear()
        self.comboBoxCategory.addItems([name for name, _ in self.productConnection.categoriesListing()])

    def changeComboBoxBrands(self):
        # Obtener la marca seleccionada
        selectedBrand = self.comboBoxBrand.currentText()

        # Limpiar y agregar elementos al ComboBox
        self.comboBoxBrand.clear()
        self.comboBoxBrand.addItems([name for name, _ in self.productConnection.brandsListing()])



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

            # Obtener el ID del proveedor seleccionado
            selectedSupplierId = self.comboBoxSupplier.currentData()
            self.product.setSupplierId(selectedSupplierId)

            # Obtener el ID de la categoría seleccionada
            selectedCategoryId = self.comboBoxCategory.currentData()
            self.product.setCategoryId(selectedCategoryId)

            # Obtener el ID de la marca seleccionada
            selectedBrandId = self.comboBoxBrand.currentData()
            self.product.setBrandId(selectedBrandId)

            if self.estado == 'AGREGAR':
                self.addProduct()
            elif self.estado == 'MODIFICAR':
                self.updateProduct()

            self.validateButtons('GUARDAR')





  


  
    def validateButtons(self, button):
        if button == 'AGREGAR' :
            self.mainWindows.wDatosProducto.setEnabled(True)
            self.mainWindows.btnDeleteProductsTab.setEnabled(True)
            self.mainWindows.btnDeleteProductsTab.setText('CANCELAR')
            self.mainWindows.btnSaveProductsTab.setEnabled(True)
            self.mainWindows.btnUpdateProductsTab.setEnabled(False)
            self.mainWindows.btnAddProductsTab.setEnabled(False)
            self.mainWindows.tvProductProductsTab.setEnabled(False)
            self.cleanFields()

        elif button=='GUARDAR':
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

        elif button=='BORRAR':
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

    def updateProduct(self):
        self.productConnection.updateProduct(self.product)
        #self.loadTable()

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
        mensaje=''
        if self.mainWindows.txtProductNameProductsTab.text() == '':
            mensaje= "Falta ingresar Nombre"
        elif self.mainWindows.txtPurchasePriceProductsTab.text() =='':
            mensaje= "Falta ingresar Precio de Compra"
        elif self.mainWindows.txtSalesPriceProductsTab.text() =='':
            mensaje= "Falta ingresar Precio de Venta"
       # elif self.supplierCompleter.currentCompletion() =='':
         #   mensaje= "Falta ingresar un Proveedor"
        #elif self.brandCompleter.currentCompletion() == '':
          #  mensaje = "Falta seleccionar la marca"
        #elif self.categoryCompleter.currentCompletion() == '':
         #   mensaje = 'Falta seleccionar el rubro'


        """elif self.supplierCompleter.currentCompletion() =='' or self.supplierCompleter.currentRow() == 0:
            mensaje= "Falta ingresar un Proveedor"
        elif self.brandCompleter.currentCompletion() == '' or self.brandCompleter.currentRow() == 0:
            mensaje = "Falta seleccionar la marca"
        elif self.categoryCompleter.currentCompletion() == '' or self.categoryCompleter.currentRow() == 0:
            mensaje = 'Falta seleccionar el rubro'
        """
        return mensaje






    def changeComboBoxSuppliers(self, index):
        # Manejar el evento de cambio de selección
        selected_supplier = self.comboBoxSupplier.currentText()
        print(f'Supplier selected: {selected_supplier}')

    def changeComboBoxCategories(self, index):
        # Manejar el evento de cambio de selección
        selected_category = self.comboBoxCategory.currentText()
        print(f'Category selected: {selected_category}')

    def changeComboBoxBrands(self, index):
        # Manejar el evento de cambio de selección
        selected_brand = self.comboBoxBrand.currentText()
        print(f'Brand selected: {selected_brand}')