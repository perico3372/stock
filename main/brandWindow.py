#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from PyQt5 import uic
from model.brand import Brand
from connection.brandConnection import BrandConnection
from model.table import TableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from model.phone import Phone
from PyQt5.QtWidgets import QMessageBox, QDialog

class BrandWindow():

    def __init__(self):

        self.brandWindow = uic.loadUi('../view/brand.ui')

        #Configurando botones
        self.barnd = Brand()
        self.brandConnection = BrandConnection()


        self.brandWindow.buttonSave.clicked.connect(self.enableButtonSave)
        self.brandWindow.buttonUpdate.clicked.connect(self.enableButtonsUpdate)
        self.brandWindow.buttonDelete.clicked.connect(self.enableButtonsDelete)
        self.brandWindow.buttonAdd.clicked.connect(self.enableButtonsAdd)

        self.brandWindow.txtFilterBrands.returnPressed.connect(self.search)

        self.brandWindow.tvBrands.setSortingEnabled(True)
        self.brandWindow.tvBrands.setMouseTracking(True)
        self.brandWindow.tvBrands.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.brandWindow.exec()

    def search(self):
        if self.brandWindow.txtFilterBrands.hasFocus() is True:
            self.loadTable()

    def enableButtonSave(self):

        if self.brandWindow.txtBrandName.text() != "":

            self.brand.setMarca(self.brandWindow.txtBrandName.text())

            if self.estado == 'ADD':
                self.addBrands()
            elif self.estado == 'UPDATE':
                self.updateBrands()
        else:
            print("Falta ingresar la descripcion")
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "Falta ingresar la descripcion")

        self.validateButtons(button='SAVE')

    def enableButtonsAdd(self):
        self.estado = 'ADD'
        self.validateButtons(button='ADD')

    def enableButtonsUpdate(self):
        self.estado='UPDATE'
        self.validateButtons(button='UPDATE')

    def enableButtonsDelete(self):
        if self.brand.getBrandId() != 0 and self.brandWindow.buttonSave.isEnabled() != True:
                self.conexionMarca.borrarMarca(self.brand)
                self.loadTable()
        self.validateButtons(button='DELETE')

    def loadTable(self):
        textFilter = self.brandWindow.txtFilterBrands.text()
        brandList = self.conexionMarca.selectMarca(textFilter)
        if len(brandList) > 0:
            #Creo la cabecera
            header = ['ID', 'Marca']
            #Creo el modelo
            self.tablaModel = MyTableModel(self.brandWindow.tvBrands, brandList, header)
            #Seteo el modelo
            self.brandWindow.tvBrands.setModel(self.tablaModel)
            self.brandWindow.tvBrands.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.brandWindow.tvBrands.setColumnHidden(0, True)
            self.brandWindow.tvBrands.setColumnWidth(1, 245)
        else:
            self.brandWindow.tvBrands.setModel(None)

    def changeSelectedTable(self, selected, deselected):
        self.brandWindow.tvBrands.selectRow(selected.row())

        brandList = selected.model().mylist
        selectBrand = brandList[selected.row()]

        self.brand = Brand()
        self.brand.setIdMarca(int(selectBrand[0]))
        self.brand.setMarca(str(selectBrand[1]))

        self.brandWindow.tvBrands.setRowHeight(deselected.row(), 33)
        self.brandWindow.tvBrands.setRowHeight(selected.row(), 45)

        self.brandWindow.txtBrandName.setText(self.brand.getMarca())
        self.brandWindow.buttonUpdate.setEnabled(True)
        self.brandWindow.buttonDelete.setEnabled(True)

    def validateButtons(self, button):
        if button == 'ADD':
            self.brandWindow.buttonUpdate.setEnabled(False)
            self.brandWindow.buttonAdd.setEnabled(False)
            self.brandWindow.buttonSave.setEnabled(True)
            self.brandWindow.buttonDelete.setText('CANCEL')
            self.brandWindow.buttonDelete.setEnabled(True)
            self.brandWindow.tvBrands.setEnabled(False)
            self.brandWindow.txtBrandName.setText('')
            self.brandWindow.txtBrandName.setEnabled(True)
        elif button == 'SAVE':
            self.brandWindow.buttonUpdate.setEnabled(False)
            self.brandWindow.buttonAdd.setEnabled(True)
            self.brandWindow.buttonSave.setEnabled(False)
            self.brandWindow.buttonDelete.setText('DELETE')
            self.brandWindow.buttonDelete.setEnabled(False)
            self.brandWindow.tvBrands.setEnabled(True)
            self.brandWindow.txtBrandName.setText('')
            self.brandWindow.txtBrandName.setEnabled(False)
        elif button == 'UPDATE':
            self.brandWindow.buttonUpdate.setEnabled(False)
            self.brandWindow.buttonAdd.setEnabled(False)
            self.brandWindow.buttonSave.setEnabled(True)
            self.brandWindow.buttonDelete.setText('CANCEL')
            self.brandWindow.buttonDelete.setEnabled(True)
            self.brandWindow.tvBrands.setEnabled(False)
            self.brandWindow.txtBrandName.setEnabled(True)
        elif button == 'DELETE':
            self.brandWindow.buttonUpdate.setEnabled(False)
            self.brandWindow.buttonAdd.setEnabled(True)
            self.brandWindow.buttonSave.setEnabled(False)
            self.brandWindow.buttonDelete.setText('DELETE')
            self.brandWindow.buttonDelete.setEnabled(False)
            self.brandWindow.tvBrands.setEnabled(True)
            self.brandWindow.txtBrandName.setText('')
            self.brandWindow.txtBrandName.setEnabled(False)

    def addBrands(self):
        if self.brand:
            self.brandConnection.addBrands(self.brand)
            self.loadTable()

    def updateBrands(self):
        if self.brand:
                self.brandConnection.updateBrands(self.brand)
                self.loadTable()