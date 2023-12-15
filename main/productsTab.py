#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.table import TableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QCompleter, QLineEdit, QComboBox, QMessageBox, QDialog, QApplication
from connection.productConnection import ProductConnection
from brandWindow import BrandWindow
from categoryWindow import CategoryWindow
from model.supplier import Supplier
from model.product import Product
from model.category import Category
from model.brand import Brand
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel, Qt
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
        self.configInit()

    def configInit(self):
        # Configurando botones
        self.mainWindows.btnAddProductsTab.clicked.connect(self.enableButtonAddProductsTab)
        self.mainWindows.btnSaveProductsTab.clicked.connect(self.enableButtonSaveProductsTab)

        # Crear instancias de QComboBox
        self.comboBoxSupplier = self.mainWindows.cbSupplierProductsTab
        self.comboBoxCategory = self.mainWindows.cbCategoryProductsTab
        self.comboBoxBrand = self.mainWindows.cbBrandProductsTab

        # Conectar la señal del comboBox a una función para manejar eventos
        self.comboBoxSupplier.currentIndexChanged.connect(self.loadSuppliersCombobox)
        self.comboBoxSupplier.currentIndexChanged.connect(self.brandsSelectionschange)
        self.comboBoxSupplier.currentIndexChanged.connect(self.categoriesSelectionschange)

        # Inicializar ComboBox
        self.loadSuppliersCombobox()
        self.loadBrandsCombobox()
        self.loadCategoriesCombobox()

        self.changeComboBoxSuppliers()
        self.changeComboBoxCategories()
        self.changeComboBoxBrands()

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



    def loadSuppliersCombobox(self):
        # Crear una instancia de la clase Connection
        productConnection = ProductConnection()

        # Obtener la lista de proveedores
        suppliersList = productConnection.suppliersListing()

        # Limpiar el comboBox antes de agregar elementos
        self.comboBoxSupplier.clear()

        # Agregar elementos al comboBox
        for supplierName, supplierId in suppliersList:
            self.comboBoxSupplier.addItem(str(supplierName), supplierId)

    def loadBrandsCombobox(self):
        # Crear una instancia de la clase Connection
        productConnection = ProductConnection()

        # Obtener la lista de marcas
        brandsList = productConnection.brandsListing()

        # Limpiar el comboBox antes de agregar elementos
        self.comboBoxBrand.clear()

        # Agregar elementos al comboBox
        for brandName, brandId in brandsList:
            self.comboBoxBrand.addItem(str(brandName), brandId)

    def loadCategoriesCombobox(self):
        # Crear una instancia de la clase Connection
        productConnection = ProductConnection()

        # Obtener la lista de categorías
        categoriesList = productConnection.categoriesListing()

        # Limpiar el comboBox antes de agregar elementos
        self.comboBoxCategory.clear()

        # Agregar elementos al comboBox
        for categoryName, categoryId in categoriesList:
            self.comboBoxCategory.addItem(str(categoryName), categoryId)

    def suppliersSelectionschange(self):
        # Manejar el cambio de selección en el comboBox
        selectedSupplierIndex = self.comboBoxSupplier.currentIndex()
        selectedSupplierId = self.comboBoxSupplier.itemData(selectedSupplierIndex, role=Qt.UserRole)
        print(f"Proveedor seleccionado: {selectedSupplierId}")

    def brandsSelectionschange(self):
        # Manejar el cambio de selección en el comboBox
        selectedBrandIndex = self.comboBoxBrand.currentIndex()
        selectedBrandId = self.comboBoxBrand.itemData(selectedBrandIndex, role=Qt.UserRole)

    def categoriesSelectionschange(self):
        # Manejar el cambio de selección en el comboBox
        selectedCategoryIndex = self.comboBoxCategory.currentIndex()
        selectedCategoryId = self.comboBoxCategory.itemData(selectedCategoryIndex, role=Qt.UserRole)

    def enableButtonAddProductsTab(self):
        self.estado = 'AGREGAR'
        self.validateButtons(button='AGREGAR')

    def enableButtonSaveProductsTab(self):

        selected_supplier_index = self.comboBoxSupplier.currentIndex()
        supplier_id = self.comboBoxSupplier.itemData(selected_supplier_index)

        validate = self.validate()

        if validate != "":
            print(validate)
            alert = QDialog()
            QMessageBox.information(alert, "ERROR", validate)
        else:
            # Obtener el ID del proveedor seleccionado
            selectedSupplierIndex = self.comboBoxSupplier.currentIndex()
            selectedSupplierId = self.comboBoxSupplier.itemData(selectedSupplierIndex, role=Qt.UserRole)

            # Establecer el ID del proveedor en el objeto supplier
            self.supplier.setPersonId(str(selectedSupplierId))

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

            self.category.setCategoryId(str(self.comboBoxCategory.currentIndexChanged.connect(self.categoriesSelectionschange)))
            # self.product.setProductCategory(self.category)

            # self.supplier.setPersonId(str(self.comboBoxSupplier.currentIndexChanged.connect(self.suppliersSelectionschange)))
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

        return mensaje
    
