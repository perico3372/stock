#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.customer import Customer
from model.table import TableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from connection.customerConnection import CustomerConnection
from model.address import Address
from connection.phoneConnection import PhoneConnection
from model.phone import Phone
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

class CustomersTab():

    def __init__(self, MainWindow):
        self.mainWindow = MainWindow
        self.customer = Customer()
        self.customerConnection = CustomerConnection()
        self.phoneConnection = PhoneConnection()

        self.InitialPhoneList = []

        self.estado = ""
        self.address = Address()

        self.configInit()


    def configInit(self):
        #Configurando botones Generales
        self.mainWindow.btnAddCustomersTab.clicked.connect(self.enableButtonAddCustomersTab)
        self.mainWindow.btnSaveCustomersTab.clicked.connect(self.enableButtonSaveCustomersTab)
        self.mainWindow.btnDeleteCustomersTab.clicked.connect(self.enableButtonDeleteCustomersTab)
        self.mainWindow.btnUpdateCustomersTab.clicked.connect(self.enableButtonUpdateCustomersTab)

        #Configurando botones ABM telefono
        self.mainWindow.btnAddPhoneCustomersTab.clicked.connect(self.enableButtonAddPhoneCustomersTab)
        self.mainWindow.btnDeletePhoneCustomersTab.clicked.connect(self.enableButtonDeletePhoneCustomersTab)
        self.mainWindow.btnCancelPhoneCustomersTab.clicked.connect(self.enableButtonCancelPhoneCustomersTab)
        self.mainWindow.btnCancelPhoneCustomersTab.setVisible(False)
        self.mainWindow.btnDeletePhoneCustomersTab.setEnabled(False)

        #configurando botones tipo telefono
        self.mainWindow.txtPhoneCustomersTab.clicked.connect(self.enableButtonPhoneCustomersTab)
        self.mainWindow.btnPhoneCellCustomersTab.clicked.connect(self.enableButtonPhoneCellCustomersTab)
        self.mainWindow.btnPhoneFaxCustomersTab.clicked.connect(self.enableButtonPhoneFaxCustomersTab)


        self.mainWindow.txtFilterCustomersCustomersTab.returnPressed.connect(self.search)

        #Seteando model y propiedades a la tabla
        self.mainWindow.tvCustomersCustomersTab.setSortingEnabled(True)
        self.mainWindow.tvCustomersCustomersTab.setMouseTracking(True)
        self.mainWindow.tvCustomersCustomersTab.setSelectionBehavior(QAbstractItemView.SelectRows)


        #Seteando proiedades de la tabla telefono
        self.mainWindow.tvPhoneCustomersTab.setSortingEnabled(True)
        self.mainWindow.tvPhoneCustomersTab.setMouseTracking(True)
        self.mainWindow.tvPhoneCustomersTab.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.mainWindow.txtFilterCustomersCustomersTab.setFocus(True)

    def finish(self):
        self.mainWindow.btnAddCustomersTab.disconnect()
        self.mainWindow.btnDeleteCustomersTab.disconnect()
        self.mainWindow.btnUpdateCustomersTab.disconnect()
        self.mainWindow.btnSaveCustomersTab.disconnect()

        self.mainWindow.btnCancelPhoneCustomersTab.disconnect()
        self.mainWindow.btnAddPhoneCustomersTab.disconnect()
        self.mainWindow.btnDeletePhoneCustomersTab.disconnect()

        self.mainWindow.btnPhoneCellCustomersTab.disconnect()
        self.mainWindow.btnPhoneFaxCustomersTab.disconnect()
        self.mainWindow.txtPhoneCustomersTab.disconnect()

        self.mainWindow.tvPhoneCustomersTab.disconnect()
        self.mainWindow.tvCustomersCustomersTab.disconnect()


    def search(self):
        if self.mainWindow.txtFilterCustomersCustomersTab.hasFocus() is True:
            self.loadTable()


    def enableButtonAddCustomersTab(self):
        self.estado = 'AGREGAR'
        self.validateButtons(button='AGREGAR')


    def enableButtonSaveCustomersTab(self):
         validate = self.validate()

         if validate != "":
             print(validate)
             alert = QDialog()
             QMessageBox.information(alert,"ERROR", validate)
         else:

             self.customer.setPersonName(str(self.mainWindow.txtCustomerNameCustomersTab.text()))
             self.customer.setPersonEmail(str(self.mainWindow.txtEmailCustomerCustomersTab.text()))

             self.customer.setAddressStreet(str(self.mainWindow.txtAddressStreetCustomersTab.text())) 
             if self.mainWindow.txtAddressNumberCustomersTab.text() != "":
                 self.customer.setAddressNumber(int(self.mainWindow.txtAddressNumberCustomersTab.text()))
             else:
                 self.customer.setAddressNumber("")
             if self.mainWindow.txtAddressFloorCustomersTab.text() != "":
                 self.customer.setAddressFloor(int(self.mainWindow.txtAddressFloorCustomersTab.text()))
             else:
                 self.customer.setAddressFloor("")
             if self.mainWindow.txtAddressDptoCustomersTab.text() != "":
                 self.customer.setAddressDpto(str(self.mainWindow.txtAddressDptoCustomersTab.text()))
             else:
                 self.customer.setAddressDpto("")

             if self.mainWindow.cbCustomerStatusCustomersTab.currentText() == 'ACTIVO':
                 self.customer.setPersonStatus(1)
             else:
                 self.customer.setPersonStatus(0)

             self.validateButtons(button='GUARDAR')

             if self.estado == 'AGREGAR':
                 self.addCustomers()
                 self.insertTelefono()
             elif self.estado == 'MODIFICAR':
                 self.updateCustomers()
                 self.updateTelefono()

    def enableButtonUpdateCustomersTab(self):
        self.estado = 'MODIFICAR'
        self.validateButtons(button='MODIFICAR')


    def enableButtonDeleteCustomersTab(self):
        if self.mainWindow.btnSaveCustomersTab.isEnabled() != True:
            self.customerConnection.deleteCustomers(self.customer)
            self.validateButtons()

        self.validateButtons(button='BORRAR')


    def loadTable(self):
        parameter = self.mainWindow.txtFilterCustomersCustomersTab.text()
        typeParameter = ''

        if self.mainWindow.cbFilterCustomersCustomersTab.currentText() == 'Nombre':
            typeParameter = 'ps.personName'
        else:
            typeParameter = 'c.customerId'

        parameterState = 1
        if self.mainWindow.cbInactiveCustomersTab.isChecked() is True:
            parameterState = 0

        customerList = self.customerConnection.customersListing(typeParameter, parameter, parameterState)

        if len(customerList) > 0:
            header = ['ID','Nombre','Email','Direccion', 'N°', 'Piso', 'Dpto', 'iddir', 'idper', 'Estado']
            self.tablaModel = TableModel(self.mainWindow.tvCustomersCustomersTab, customerList, header)
            self.mainWindow.tvCustomersCustomersTab.setModel(self.tablaModel)
            self.mainWindow.tvCustomersCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(0, True)
            self.mainWindow.tvCustomersCustomersTab.setColumnWidth(1, 220)
            self.mainWindow.tvCustomersCustomersTab.setColumnWidth(2, 280)
            self.mainWindow.tvCustomersCustomersTab.setColumnWidth(3, 364)
            self.mainWindow.tvCustomersCustomersTab.setColumnWidth(4, 50)
            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(5, 50)
            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(6, 50)
            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(7, True)
            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(8, True)
            self.mainWindow.tvCustomersCustomersTab.setColumnHidden(9, True)
        else:
            self.mainWindow.tvCustomersCustomersTab.setModel(None)


    def changeSelectedTable(self, selected, deselected):

            customerlist = selected.model().mylist
            selectedCustomer = customerlist[selected.row()]
            self.customer = Customer()
            self.address = Address()
            self.customer.setCustomerId(int(selectedCustomer[0]))
            self.customer.setPersonName(selectedCustomer[1])
            self.customer.setPersonEmail(selectedCustomer[2])
            self.address.setDireccion(selectedCustomer[3])
            if selectedCustomer[4] != None:
                self.address.setAddressNumber(int(selectedCustomer[4]))
            if selectedCustomer[5] != None:
                self.address.setAddressFloor(int(selectedCustomer[5]))
            if selectedCustomer[6] != None:
                self.address.setAddressDpto(selectedCustomer[6])
            self.address.setAddressId(int(selectedCustomer[7]))
            self.customer.setPersonId(selectedCustomer[8])

            self.mainWindow.tvCustomersCustomersTab.setRowHeight(deselected.row(), 28)
            self.mainWindow.tvCustomersCustomersTab.setRowHeight(selected.row(), 45)

            self.customer.setCustomerStatus(int(selectedCustomer[10]))

            self.setFields()
            self.mainWindow.btnUpdateCustomersTab.setEnabled(True)
            self.mainWindow.btnDeleteCustomersTab.setEnabled(True)
            self.mainWindow.tvPhoneCustomersTab.setModel(None)
            self.loadPhoneTable()


    def validateButtons(self, button):
        if button == 'AGREGAR' :
            self.mainWindow.wDatosCliente.setEnabled(True)
            self.mainWindow.btnDeleteCustomersTab.setEnabled(True)
            self.mainWindow.btnDeleteCustomersTab.setText('CANCELAR')
            self.mainWindow.btnSaveCustomersTab.setEnabled(True)
            self.mainWindow.btnUpdateCustomersTab.setEnabled(False)
            self.mainWindow.btnAddCustomersTab.setEnabled(False)
            self.mainWindow.tvCustomersCustomersTab.setEnabled(False)
            self.cleanFields()

        elif button=='GUARDAR':
            self.mainWindow.btnUpdateCustomersTab.setEnabled(False)
            self.mainWindow.btnAddCustomersTab.setEnabled(True)
            self.mainWindow.btnSaveCustomersTab.setEnabled(False)
            self.mainWindow.btnDeleteCustomersTab.setText('BORRAR')
            self.mainWindow.btnDeleteCustomersTab.setEnabled(False)
            self.mainWindow.tvCustomersCustomersTab.setEnabled(True)
            self.mainWindow.wDatosCliente.setEnabled(False)
            self.cleanFields()

        elif button == 'MODIFICAR':
            self.mainWindow.btnUpdateCustomersTab.setEnabled(False)
            self.mainWindow.btnAddCustomersTab.setEnabled(False)
            self.mainWindow.btnSaveCustomersTab.setEnabled(True)
            self.mainWindow.btnDeleteCustomersTab.setText('Cancelar')
            self.mainWindow.btnDeleteCustomersTab.setEnabled(True)
            self.mainWindow.tvCustomersCustomersTab.setEnabled(False)
            self.mainWindow.wDatosCliente.setEnabled(True)

        elif button=='BORRAR':
            self.mainWindow.btnUpdateCustomersTab.setEnabled(False)
            self.mainWindow.btnAddCustomersTab.setEnabled(True)
            self.mainWindow.btnSaveCustomersTab.setEnabled(False)
            self.mainWindow.btnDeleteCustomersTab.setText('BORRAR')
            self.mainWindow.btnDeleteCustomersTab.setEnabled(False)
            self.mainWindow.tvCustomersCustomersTab.setEnabled(True)
            self.mainWindow.wDatosCliente.setEnabled(False)
            self.cleanFields()


    def addCustomers(self):
        if self.customer.getPersonName() != '':
            self.customerConnection.addCustomers(customer=self.customer)
            self.loadTable()

    def updateCustomers(self):
            self.customerConnection.updateCustomers(self.customer)
            self.loadTable()

    def cleanFields(self):
       # self.mainWindow.txtApellido_c.setText('')
        self.mainWindow.txtCustomerNameCustomersTab.setText('')
        self.mainWindow.txtAddressStreetCustomersTab.setText('')
        self.mainWindow.txtAddressNumberCustomersTab.setText('')
        self.mainWindow.txtAddressFloorCustomersTab.setText('')
        self.mainWindow.txtAddressDptoCustomersTab.setText('')
        self.mainWindow.txtEmailCustomerCustomersTab.setText('')
        self.mainWindow.tvPhoneCustomersTab.setModel(None)
        self.mainWindow.cbCustomerStatusCustomersTab.setCurrentIndex(0)
        self.mainWindow.txtFilterCustomersCustomersTab.setText('')
        self.mainWindow.tvCustomersCustomersTab.setModel(None)
        self.mainWindow.txtFilterCustomersCustomersTab.setFocus(True)

    def setFields(self):
       # self.mainWindow.txtApellido_c.setText(self.customer.getApellido())
        self.mainWindow.txtCustomerNameCustomersTab.setText(self.customer.getPersonName())
        self.mainWindow.txtEmailCustomerCustomersTab.setText(self.customer.getPersonEmail())
        self.mainWindow.txtAddressStreetCustomersTab.setText(self.customer.getAddressStreet())        
        if self.customer.getAddressNumber() != None:
            self.mainWindow.txtAddressNumberCustomersTab.setText(str(self.customer.getAddressNumber()))
        else:
            self.mainWindow.txtAddressNumberCustomersTab.setText('')            
        if self.customer.getAddressFloor() != None:
            self.mainWindow.txtAddressFloorCustomersTab.setText(str(self.customer.getAddressFloor()))
        else:
            self.mainWindow.txtAddressFloorCustomersTab.setText('')
        if self.customer.getAddressDpto() != None:
            self.mainWindow.txtAddressDptoCustomersTab.setText(self.customer.getAddressDpto())
        else:
            self.mainWindow.txtAddressDptoCustomersTab.setText('')
        if self.customer.getPersonStatus() == 1:
            self.mainWindow.btnCustomerStatusCustomersTab.setCurrentIndex(0)
        else:
            self.mainWindow.btnCustomerStatusCustomersTab.setCurrentIndex(1)

    def validate(self):
        mensaje = ''
        if self.mainWindow.txtCustomerNameCustomersTab.text() == '':
            mensaje = "Falta ingresar un Nombre"
        elif self.mainWindow.txtCustomerNameCustomersTab.text() == '':
            mensaje = "Falta ingresar Apellido"
        elif self.mainWindow.txtAddressStreetCustomersTab.text() == '':
            mensaje = "Falta ingresar una Direccion"
        elif self.mainWindow.txtAddressNumberCustomersTab.text() == '':
            mensaje = "Falta ingresar un N° de Direccion"

        return mensaje


    def loadPhoneTable(self):
        self.InitialPhoneList = self.phoneConnection.selectTelefono(self.customer)
        if len(self.InitialPhoneList) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = TableModel(self.mainWindow, self.InitialPhoneList, header)
            self.mainWindow.tvPhoneCustomersTab.setModel(tableModel)
            self.mainWindow.tvPhoneCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.mainWindow.tvPhoneCustomersTab.setColumnHidden(0, True)
            self.mainWindow.tvPhoneCustomersTab.setColumnWidth(1, 36)
            self.mainWindow.tvPhoneCustomersTab.setColumnWidth(2, 175)

            for r in range(0, len(self.InitialPhoneList)):
                self.mainWindow.tvPhoneCustomersTab.setRowHidden(r, False)


    def changeSelectedTableTel(self, selected, deselected):
        listTelefonos = selected.model().mylist
        self.selectedPhone = ()
        self.selectedPhone = listTelefonos[selected.row()]

        self.telefonoSelectedRow = selected.row()
        self.mainWindow.txtPhoneCustomersTab.setText(str(self.selectedPhone[2]))

        self.setPhoneType(str(self.selectedPhone[1]))
        self.mainWindow.btnCancelPhoneCustomersTab.setVisible(True)
        self.mainWindow.btnDeletePhoneCustomersTab.setEnabled(True)
        self.mainWindow.tvPhoneCustomersTab.setEnabled(False)

        self.mainWindow.btnSaveCustomersTab.setEnabled(False)
        self.mainWindow.btnDeleteCustomersTab.setEnabled(False)

    def updateTelefono(self):

        phoneList = []
        if self.mainWindow.tvPhoneCustomersTab.model() != None and \
                        len(self.mainWindow.tvPhoneCustomersTab.model().mylist) > 0:
            phoneList = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()

            estado = ''
            telNew = Phone()
            if len(phoneList) > 0:
                if len(self.phoneListsInit) > 0:

                    listTelInit = list(self.listTelefonosInit)
                    parche = (phoneList[0][0], phoneList[0][1], str(phoneList[0][2]))
                    phoneList[0] = parche
                    #Recorre la lista de telefono inicial
                    for telInit in listTelInit:
                        #recorre la lista de telefonos nueva
                        for tel in phoneList:
                            telNew.setPersonId(self.customer.getPersonId())
                            telNew.setPhoneId(tel[0])
                            telNew.setPhoneType(tel[1])
                            if tel[2] == "":
                                estado = 'DEL'
                                break
                            else:
                                telNew.setTelefono(tel[2])

                            if tel[0] == 0:
                                estado = 'INS'
                                break

                            if telInit[0] == tel[0]:
                                if telInit[1] != tel[1] or telInit[2] != tel[2]:
                                    estado = 'UPD'
                                    break

                        if estado == 'UPD':
                            self.phoneConnection.updatePhone(telNew)
                        elif estado == "INS":
                            self.phoneConnection.addPhone(telNew)
                        elif estado == 'DEL':
                            self.phoneConnection.deletePhone(telNew)
                #Si la lista de telefono inicial es cero
                else:
                    #recorre la lista de telefonos nueva para agregarlos a todos
                    for telN in phoneList:
                        if telN[2] != '':
                            telNew = Phone()
                            telNew.setPersonId(self.customer.getPersonId())
                            telNew.setPhoneId(telN[0])
                            telNew.setPhoneType(telN[1])
                            telNew.setPhoneNumber(telN[2])
                            self.phoneConnection.insertarTelefono(telNew)

    def addPhoneCustomersTab(self):

        newPhoneList = []
        tel = self.mainWindow.tvPhoneCustomersTab.model()

        newPhoneList = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()

        if len(newPhoneList) > 0:
            self.phoneConnection.addPhoneInit(newPhoneList)


    def enableButtonCancelPhoneCustomersTab(self):
        self.mainWindow.btnCancelPhoneCustomersTab.setVisible(False)
        self.mainWindow.txtPhoneCustomersTab.setText('')

        self.mainWindow.btnDeletePhoneCustomersTab.setEnabled(False)
        self.mainWindow.tvPhoneCustomersTab.clearSelection()
        self.mainWindow.tvPhoneCustomersTab.setEnabled(True)

        self.mainWindow.btnSaveCustomersTab.setEnabled(True)
        self.mainWindow.btnDeleteCustomersTab.setEnabled(True)


    def enableButtonAddPhoneCustomersTab(self):
        phoneNumber = self.mainWindow.txtPhoneCustomersTab.text()

        if phoneNumber.isdigit() == True:
            if self.mainWindow.btnCancelPhoneCustomersTab.isVisible() is True:
                self.updateTelefonoTabla()
            else:
                self.addPhoneTable()

            self.mainWindow.tvPhoneCustomersTab.clearSelection()
            self.mainWindow.btnDeletePhoneCustomersTab.setEnabled(False)
            self.mainWindow.btnCancelPhoneCustomersTab.setVisible(False)
            self.mainWindow.txtPhoneCustomersTab.setText('')
            self.mainWindow.tvPhoneCustomersTab.setEnabled(True)

            self.mainWindow.btnSaveCustomersTab.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def enableButtonDeletePhoneCustomersTab(self):
        listTabTel = []
        #listTabTel = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()
        #tipoTel = str(self.getTypePhone())
        newPhoneList = []

        listTabTel = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.selectedPhone[0], self.selectedPhone[1], '']
        listTabTel[self.selectedPhoneRow] = telDel
        tableTelModel = TableModel(self.mainWindow, listTabTel, header)
        self.mainWindow.tvPhoneCustomersTab.setModel(tableTelModel)
        self.mainWindow.tvPhoneCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.mainWindow.tvPhoneCustomersTab.setRowHidden(self.telefonoSelectedRow, True)

        self.mainWindow.btnCancelPhoneCustomersTab.setVisible(False)
        self.mainWindow.txtPhoneCustomersTab.setText('')
        self.mainWindow.btnDeletePhoneCustomersTab.setEnabled(False)
        self.mainWindow.tvPhoneCustomersTab.setEnabled(True)

        self.mainWindow.btnSaveCustomersTab.setEnabled(True)
        self.mainWindow.btnDeleteCustomersTab.setEnabled(True)


    def enableButtonPhoneCustomersTab(self):
        self.changeTypePhone(button='TEL')


    def enableButtonPhoneCellCustomersTab(self):
        self.changeTypePhone(button='CEL')


    def enableButtonPhoneFaxCustomersTab(self):
        self.changeTypePhone(button='FAX')


    def changeTypePhone(self, button):

        if button == 'TEL':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(False)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(True)
        elif button == 'CEL':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(False)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(True)
        elif button == 'FAX':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(False)


    def setPhoneType(self, typePhone):

        if typePhone == 'TEL':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(False)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(True)
        elif typePhone == 'CEL':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(False)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(True)
        elif typePhone == 'FAX':
            self.mainWindow.txtPhoneCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellCustomersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxCustomersTab.setEnabled(False)


    def getTypePhone(self):

        if self.mainWindow.txtPhoneCustomersTab.isEnabled() != True:
            return 'TEL'
        elif self.mainWindow.btnPhoneCellCustomersTab.isEnabled() != True:
            return 'CEL'
        elif self.mainWindow.btnPhoneFaxCustomersTab.isEnabled() != True:
            return 'FAX'


    def addPhoneTable(self):
        phoneNumber = self.mainWindow.txtPhoneCustomersTab.text()
        tipoTel = str(self.getTypePhone())

        phoneModelList = self.mainWindow.tvPhoneCustomersTab.model()
        header = ['ID', 'Tipo', 'Numero']

        if phoneModelList is not None:
            listTabTel = list(self.mainWindow.tvPhoneCustomersTab.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, phoneNumber )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = TableModel(self.mainWindow, tupleTable , header)
                self.mainWindow.tvPhoneCustomersTab.setModel(tableModel)
                self.mainWindow.tvPhoneCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, phoneNumber )
            lista.append(tuplaTel)

            tableModel = TableModel(self.mainWindow, lista , header)
            self.mainWindow.tvPhoneCustomersTab.setModel(tableModel)
            self.mainWindow.tvPhoneCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.mainWindow.tvPhoneCustomersTab.setColumnHidden(0, True)
            self.mainWindow.tvPhoneCustomersTab.setColumnWidth(1, 36)
            self.mainWindow.tvPhoneCustomersTab.setColumnWidth(2, 175)


    def updateTelefonoTabla(self):
        listTabTel = []
        #listTabTel = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()
        tipoTel = str(self.getTypePhone())
        newPhoneList = []
        #prob = self.mainWindow.tvPhoneCustomersTab.selectionModel()
        #prob1 = self.mainWindow.tvPhoneCustomersTab.model()
        listTabTel = list(self.mainWindow.tvPhoneCustomersTab.model().mylist).copy()
        """
        for lt in listTabTel:
            if lt[0] == self.telefonoSelected[0]:
                lt = (self.telefonoSelected[0], tipoTel, self.mainWindow.txtPhoneCustomersTab.text())

            newPhoneList.append(lt)
        """
        telUpd = (self.telefonoSelected[0], tipoTel, int(self.mainWindow.txtPhoneCustomersTab.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = TableModel(self.mainWindow, listTabTel , header)
        self.mainWindow.tvPhoneCustomersTab.setModel(tableModel)
        self.mainWindow.tvPhoneCustomersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)