#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QDialog
from model.category import Category
from model.table import TableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from connection.categoryConnection import CategoryConnection
from model.phone import Phone


class CategoryWindow():

    def __init__(self):

        #Definiendo variables
        self.categoryWindow = uic.loadUi('../wiew/category.ui')
        self.category = Category()
        self.categoryConnection = CategoryConnection()
        self.contAttr = 0
        self.status = "" #Variable donde guardo el status, para saber que accion hace el boton guardar.
        #Configurando botones
        self.categoryWindow.buttonSave.clicked.connect(self.enableButtonCategorySave)
        self.categoryWindow.buttonUpdate.clicked.connect(self.enableButtonCategoryUpdate)
        self.categoryWindow.buttonDelete.clicked.connect(self.enableButtonCategoryDelete)
        self.categoryWindow.buttonAdd.clicked.connect(self.enableButtonCategoryAdd)

        self.categoryWindow.txtFilterCategory.returnPressed.connect(self.search)

        #Seteo propiedades de la tabla
        self.categoryWindow.tvCategories.setSortingEnabled(True)
        self.categoryWindow.tvCategories.setMouseTracking(True)
        self.categoryWindow.tvCategories.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.categoryWindow.exec()
        #sys.executable(self.categoryWindow.exec_())


    def search(self):
        if self.categoryWindow.txtFilterCategory.hasFocus() is True:
            self.loadTable()

    def enableButtonCategorySave(self):

        if self.categoryWindow.txtCategoryName.text() != "":

            self.category.setRubro(self.categoryWindow.txtCategoryName.text())

            if self.status == 'ADD':
                self.insertRubro()
            elif self.status == 'UPDATE':
                self.modificarRubro()
        else:
            print("Falta completar el campo descripcion")
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "Falta completar el campo descripcion")

        self.validarBotones(button='SAVE')


    def enableButtonCategoryAdd(self):
        self.status = 'ADD'
        self.validarBotones(button='ADD')

    def enableButtonCategoryUpdate(self):
        self.status = 'UPDATE'
        self.validarBotones(button='UPDATE')

    def enableButtonCategoryDelete(self):
        if self.category and self.categoryWindow.buttonAdd.isEnabled():
            self.categoryConnection.deleteCategory(self.category)
            self.loadTable()
        self.validarBotones(button='DELETE')

    def loadTable(self):
        #Seteo el dataProvider de la tabla
        filterText = self.categoryWindow.txtFilterCategory.text()
        categoryList = self.categoryConnection.selectCategory(filterText)
        if len(categoryList) > 0:
            header = ['ID', 'categoría']
            self.tablaModel = MyTableModel(self.categoryWindow.tvCategories, categoryList, header)
            self.categoryWindow.tvCategories.setModel(self.tablaModel)
            self.categoryWindow.tvCategories.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.categoryWindow.tvCategories.setColumnHidden(0, True)
            self.categoryWindow.tvCategories.setColumnWidth(1, 245)
        else:
            self.categoryWindow.tvCategories.setModel(None)

    def changeSelectedTable(self, selected, deselected):
        self.categoryWindow.tvCategories.selectRow(selected.row())

        categoryList = selected.model().mylist
        selectCategory = categoryList[selected.row()]

        self.category = Category()
        self.category.setCategoryId(int(selectCategory[0]))
        self.category.setCategoryName(str(selectCategory[1]))

        self.categoryWindow.tvCategories.setRowHeight(deselected.row(), 33)
        self.categoryWindow.tvCategories.setRowHeight(selected.row(), 45)

        self.categoryWindow.txtCategoryName.setText(str(self.category.getCategoryName()))
        self.categoryWindow.buttonUpdate.setEnabled(True)
        self.categoryWindow.buttonDelete.setEnabled(True)


    def validateButtons(self, button):
        if button == 'ADD':
            self.categoryWindow.buttonUpdate.setEnabled(False)
            self.categoryWindow.buttonAdd.setEnabled(False)
            self.categoryWindow.buttonSave.setEnabled(True)
            self.categoryWindow.buttonDelete.setText('CANCEL')
            self.categoryWindow.buttonDelete.setEnabled(True)
            self.categoryWindow.tvCategories.setEnabled(False)
            self.categoryWindow.txtCategoryName.setText('')
            self.categoryWindow.txtCategoryName.setEnabled(True)
        elif button == 'SAVE':
            self.categoryWindow.buttonUpdate.setEnabled(False)
            self.categoryWindow.buttonAdd.setEnabled(True)
            self.categoryWindow.buttonSave.setEnabled(False)
            self.categoryWindow.buttonDelete.setText('DELETE')
            self.categoryWindow.buttonDelete.setEnabled(False)
            self.categoryWindow.tvCategories.setEnabled(True)
            self.categoryWindow.txtCategoryName.setText('')
            self.categoryWindow.txtCategoryName.setEnabled(False)
        elif button == 'UPDATE':
            self.categoryWindow.buttonUpdate.setEnabled(False)
            self.categoryWindow.buttonAdd.setEnabled(False)
            self.categoryWindow.buttonSave.setEnabled(True)
            self.categoryWindow.buttonDelete.setText('CANCEL')
            self.categoryWindow.buttonDelete.setEnabled(True)
            self.categoryWindow.tvCategories.setEnabled(False)
            self.categoryWindow.txtCategoryName.setEnabled(True)
        elif button == 'DELETE':
            self.categoryWindow.buttonUpdate.setEnabled(False)
            self.categoryWindow.buttonAdd.setEnabled(True)
            self.categoryWindow.buttonSave.setEnabled(False)
            self.categoryWindow.buttonDelete.setText('DELETE')
            self.categoryWindow.buttonDelete.setEnabled(False)
            self.categoryWindow.tvCategories.setEnabled(True)
            self.categoryWindow.txtCategoryName.setText('')
            self.categoryWindow.txtCategoryName.setEnabled(False)

    def addCategory(self):
        if self.category:
            self.categoryConnection.addCategory(self.category)
            self.loadTable()

    def updateCategory(self):
         if self.category:
            self.categoryConnection.updateCategory(self.category)
            self.loadTable()
