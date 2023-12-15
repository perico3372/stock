

import sys
sys.path.append('..')


from model.supplier import Supplier
from model.person import Person
from connection.supplierConnection import SupplierConnection
from PyQt5.QtWidgets import QAbstractItemView, QTableView
from model.table import TableModel
from model.address import Address
from connection.phoneConnection import PhoneConnection
from model.phone import Phone
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtCore, QtGui

class SuppliersTab():

    def __init__(self, mainWindow):
        self.supplier = Supplier()
        self.mainWindow = mainWindow

        self.supplierConnection = SupplierConnection()
        self.phoneConnection = PhoneConnection()
        self.estado = ""
        self.address = Address()
        #self.tvPhoneSuppliersTab = QTableView(self)
        #self.tvPhoneSuppliersTab = QTableView(mainWindow)
        self.configInit()


    def configInit(self):
        """
        Configuracion inicial de la pestaña probeedor, setea todas las señales de los botones y carga la tabla
        @return: void
        """
         #Configurando botones Generales
        self.mainWindow.btnSaveSuppliersTab.clicked.connect(self.enableButtonSaveSuppliersTab)
        self.mainWindow.btnAddSuppliersTab.clicked.connect(self.enableButtonAdd)
        self.mainWindow.btnUpdateSuppliersTab.clicked.connect(self.enableButtonUpdate)
        self.mainWindow.btnDeleteSuppliersTab.clicked.connect(self.enableButtonDelete)

        #Configurando botones ABM telefono
        self.mainWindow.btnSumarTelefono_prov.clicked.connect(self.enableButtonAddPhone)
        self.mainWindow.btnRestarTelefono_prov.clicked.connect(self.enableButtonDeletePhone)
        self.mainWindow.btnCancelarTelefono_prov.clicked.connect(self.onClickCancelarTelefono)
        self.mainWindow.btnCancelarTelefono_prov.setVisible(False)
        self.mainWindow.btnRestarTelefono_prov.setEnabled(False)

        #configurando botones tipo telefono
        self.mainWindow.btnPhoneSuppliersTab.clicked.connect(self.enableButtonPhone)
        self.mainWindow.btnPhoneCellSuppliersTab.clicked.connect(self.enableButtonPhoneCell)
        self.mainWindow.btnPhoneFaxSuppliersTab.clicked.connect(self.enableButtonPhoneFax)

        self.mainWindow.txtFilterSuppliersSuppliersTab.returnPressed.connect(self.search)

        #Seteando model y propieades de la tabla
        self.mainWindow.tvSuppliersSuppliersTab.setSortingEnabled(True)
        self.mainWindow.tvSuppliersSuppliersTab.setMouseTracking(True)
        self.mainWindow.tvSuppliersSuppliersTab.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        #Seteando proiedades de la tabla telefono
        self.mainWindow.tvPhoneSuppliersTab.setSortingEnabled(True)
        self.mainWindow.tvPhoneSuppliersTab.setMouseTracking(True)
        self.mainWindow.tvPhoneSuppliersTab.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.mainWindow.txtFilterSuppliersSuppliersTab.setFocus(True)


    def finish(self):
        self.mainWindow.btnAddSuppliersTab.disconnect()
        self.mainWindow.btnDeleteSuppliersTab.disconnect()
        self.mainWindow.btnUpdateSuppliersTab.disconnect()
        self.mainWindow.btnSaveSuppliersTab.disconnect()

        self.mainWindow.btnCancelarTelefono_prov.disconnect()
        self.mainWindow.btnSumarTelefono_prov.disconnect()
        self.mainWindow.btnRestarTelefono_prov.disconnect()

        self.mainWindow.btnPhoneCellSuppliersTab.disconnect()
        self.mainWindow.btnPhoneFaxSuppliersTab.disconnect()
        self.mainWindow.btnPhoneSuppliersTab.disconnect()

        self.mainWindow.tvPhoneSuppliersTab.disconnect()
        self.mainWindow.tvSuppliersSuppliersTab.disconnect()

    def search(self):
        if self.mainWindow.txtFilterSuppliersSuppliersTab.hasFocus() is True:
            self.loadTable()

    def enableButtonAdd(self):
        self.estado = 'AGREGAR'
        self.validateButtons(button='AGREGAR')




    def enableButtonSaveSuppliersTab(self):
         validate = self.validate()

         if validate != "":
             print(validate)
             alert = QDialog()
             QMessageBox.information(alert,"ERROR", validate)
         else:

             self.supplier.setPersonName(str(self.mainWindow.txtSupplierNameSuppliersTab.text()))


             self.supplier.setPersonEmail(str(self.mainWindow.txtEmailSuppliersTab.text()))
             self.supplier.setSupplierWeb(str(self.mainWindow.txtSupplierWebSuupliersTab.text()))
             self.supplier.setAddressStreet(str(self.mainWindow.txtAddressStreetSuppliersTab.text())) 
             if self.mainWindow.txtAddressNumberSupliersTab.text() != "":
                 self.supplier.setAddressNumber(int(self.mainWindow.txtAddressNumberSupliersTab.text()))
             else:
                 self.supplier.setAddressNumber("")
             if self.mainWindow.txtAddressFloorSuppliersTab.text() != "":
                 self.supplier.setAddressFloor(int(self.mainWindow.txtAddressFloorSuppliersTab.text()))
             else:
                 self.supplier.setAddressFloor("")
             if self.mainWindow.txtAddressDptoSuppliersTab.text() != "":
                 self.supplier.setAddressDpto(str(self.mainWindow.txtAddressDptoSuppliersTab.text()))
             else:
                 self.supplier.setAddressDpto("")

             if self.mainWindow.cbSupplierStatusSuppliersTab.currentText() == 'ACTIVO':
                 self.supplier.setPersonStatus(1)
             else:
                 self.supplier.setPersonStatus(0)

             self.validateButtons(button='GUARDAR')

             if self.estado == 'AGREGAR':
                 self.addSuppliers()
                 self.insertTelefono()
             elif self.estado == 'MODIFICAR':
                 self.updateSuppliers()
                 self.updateTelefono()





    def enableButtonUpdate(self):
        self.estado = 'MODIFICAR'
        self.validateButtons(button='MODIFICAR')


    def enableButtonDelete(self):

        if self.mainWindow.btnSaveSuppliersTab.isEnabled() != True:
            self.supplierConnection.deleteSuppliers(self.supplier)
            self.loadTable()

        self.validateButtons(button='BORRAR')


    def loadTable(self):
        parameter = self.mainWindow.txtFilterSuppliersSuppliersTab.text()
        typeParameter = ''

        if self.mainWindow.cbFilterSupplierSuppliersTab.currentText() == 'ID':
            typeParameter = 's.supplierId'
        else:
            typeParameter = 'ps.personName'

        parameterState = 1
        if self.mainWindow.cbInactiveSuppliersTab.isChecked() is True:
            parameterState = 0

        suppliersList = self.supplierConnection.suppliersListing(typeParameter, parameter, parameterState)

        if len(suppliersList) > 0:
            header = ['ID', 'Descripcion', 'Nombre', 'Email', 'Web', 'Calle', 'N°', 'P', 'D', 'idper', 'iddir', 'Estado' ]
            tableModel = TableModel(self.mainWindow.tvSuppliersSuppliersTab, suppliersList, header)
            self.mainWindow.tvSuppliersSuppliersTab.setModel(tableModel)
            self.mainWindow.tvSuppliersSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(0, True)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(1, 190)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(2, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(3, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(4, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(5, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnWidth(6, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(7, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(8, 100)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(9, True)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(10, True)
            self.mainWindow.tvSuppliersSuppliersTab.setColumnHidden(11, True)
        else:
            self.mainWindow.tvSuppliersSuppliersTab.setModel(None)


    def changeSelectedTable(self, selected, deselected):
        supplierList = selected.model().mylist
        selectedSupplier = supplierList[selected.row()]
        self.supplier = Supplier()
        self.address = Address()
        self.supplier.setSupplierId(int(selectedSupplier[0]))
        self.supplier.setSupplierDescription(str(selectedSupplier[1]))
        self.supplier.setPersonName(str(selectedSupplier[2]))
        self.supplier.setPersonEmail(str(selectedSupplier[3]))
        self.supplier.setSupplierWeb(str(selectedSupplier[4]))
        self.supplier.setAddressStreet(str(selectedSupplier[5]))
        if selectedSupplier[6] != None:
            self.supplier.setAddressNumber(int(selectedSupplier[6]))
        if selectedSupplier[7] != None:
            self.supplier.setAddressFloor(int(selectedSupplier[7]))
        if selectedSupplier[8] != None:
            self.supplier.setAddressDpto(selectedSupplier[8])
        self.address.setPersonId(int(selectedSupplier[9]))
        self.supplier.setAddressId(int(selectedSupplier[10]))
        self.supplier.setPersonStatus(int(selectedSupplier[11]))
        self.mainWindow.tvSuppliersSuppliersTab.setRowHeight(deselected.row(), 28)
        self.mainWindow.tvSuppliersSuppliersTab.setRowHeight(selected.row(), 45)

        self.setFields()
        self.mainWindow.btnUpdateSuppliersTab.setEnabled(True)
        self.mainWindow.btnDeleteSuppliersTab.setEnabled(True)
        self.mainWindow.tvPhoneSuppliersTab.setModel(None)
        self.phoneLoadTable()


    def validateButtons(self, button):

        if button == 'AGREGAR':
            self.mainWindow.btnAddSuppliersTab.setEnabled(False)
            self.mainWindow.btnUpdateSuppliersTab.setEnabled(False)
            self.mainWindow.btnSaveSuppliersTab.setEnabled(True)
            self.mainWindow.btnDeleteSuppliersTab.setEnabled(True)
            self.mainWindow.tvSuppliersSuppliersTab.setEnabled(False)
            self.mainWindow.wDatosProveedor.setEnabled(True)
            self.mainWindow.btnDeleteSuppliersTab.setText('CANCELAR')
            self.limpiarCampos()
        elif button == 'GUARDAR':
            self.mainWindow.btnAddSuppliersTab.setEnabled(True)
            self.mainWindow.btnUpdateSuppliersTab.setEnabled(False)
            self.mainWindow.btnSaveSuppliersTab.setEnabled(False)
            self.mainWindow.btnDeleteSuppliersTab.setEnabled(False)
            self.mainWindow.tvSuppliersSuppliersTab.setEnabled(True)
            self.mainWindow.wDatosProveedor.setEnabled(False)
            self.mainWindow.btnDeleteSuppliersTab.setText('BORRAR')
            self.limpiarCampos()
        elif button == 'MODIFICAR':
            self.mainWindow.btnAddSuppliersTab.setEnabled(False)
            self.mainWindow.btnUpdateSuppliersTab.setEnabled(False)
            self.mainWindow.btnSaveSuppliersTab.setEnabled(True)
            self.mainWindow.btnDeleteSuppliersTab.setEnabled(True)
            self.mainWindow.tvSuppliersSuppliersTab.setEnabled(False)
            self.mainWindow.wDatosProveedor.setEnabled(True)
            self.mainWindow.btnDeleteSuppliersTab.setText('CANCELAR')
        elif button == 'BORRAR':
            self.mainWindow.btnAddSuppliersTab.setEnabled(True)
            self.mainWindow.btnUpdateSuppliersTab.setEnabled(False)
            self.mainWindow.btnSaveSuppliersTab.setEnabled(False)
            self.mainWindow.btnDeleteSuppliersTab.setEnabled(False)
            self.mainWindow.tvSuppliersSuppliersTab.setEnabled(True)
            self.mainWindow.wDatosProveedor.setEnabled(False)
            self.mainWindow.btnDeleteSuppliersTab.setText('BORRAR')
            self.limpiarCampos()


    def addSuppliers(self):
        self.supplierConnection.addSuppliers(supplier=self.supplier)
        self.loadTable()


    def updateSuppliers(self):
        self.supplierConnection.updateSuppliers(supplier=self.supplier)
        self.loadTable()


    # def limpiarCampos(self):
    #     self.mainWindow.txtSupplierNameSuppliersTab.setText('')
    #     self.mainWindow.txtDesscriptionSuppliersTab.setText('')
    #     self.mainWindow.txtEmailSuppliersTab.setText('')
    #     self.mainWindow.txtAddressStreetSuppliersTab.setText('')
    #     self.mainWindow.txtAddressNumberSupliersTab.setText('')
    #     self.mainWindow.txtAddressFloorSuppliersTab.setText('')
    #     self.mainWindow.txtAddressDptoSuppliersTab.setText('')
    #     self.mainWindow.txtSupplierWebSuupliersTab.setText('')
    #     self.mainWindow.tvPhoneSuppliersTab.setModel(None)
    #     self.mainWindow.cbSupplierStatusSuppliersTab.setCurrentIndex(0)
    #     self.mainWindow.txtFilterSuppliersSuppliersTab.setText('')
    #     self.mainWindow.tvSuppliersSuppliersTab.setModel(None)

    #     self.mainWindow.txtFilterSuppliersSuppliersTab.setFocus(True)
    
    def limpiarTabla(self, tableView):
        model = tableView.model()
        if model is not None:
            if hasattr(model, 'clear'):
                model.clear()
                tableView.setModel(None)
    
    
    def limpiarCampos(self):
        self.mainWindow.txtSupplierNameSuppliersTab.setText('')
        self.mainWindow.txtDesscriptionSuppliersTab.setText('')
        self.mainWindow.txtEmailSuppliersTab.setText('')
        self.mainWindow.txtAddressStreetSuppliersTab.setText('')
        self.mainWindow.txtAddressNumberSupliersTab.setText('')
        self.mainWindow.txtAddressFloorSuppliersTab.setText('')
        self.mainWindow.txtAddressDptoSuppliersTab.setText('')
        self.mainWindow.txtSupplierWebSuupliersTab.setText('')
        
        
        #self.mainWindow.tvPhoneSuppliersTab.setModel(None)
        #self.limpiarTabla(self.mainWindow.tvPhoneSuppliersTab)
        
        self.limpiarTabla(self.mainWindow.tvPhoneSuppliersTab)
        
        
        self.mainWindow.cbSupplierStatusSuppliersTab.setCurrentIndex(0)
        self.mainWindow.txtFilterSuppliersSuppliersTab.setText('')
        

    
        self.mainWindow.txtFilterSuppliersSuppliersTab.setFocus(True)





    def setFields(self):
        self.mainWindow.txtSupplierNameSuppliersTab.setText(str(self.supplier.getPersonName()))
       # self.mainWindow.txtDesscriptionSuppliersTab.setText(str(self.supplier.getSupplierDescription()))
        self.mainWindow.txtEmailSuppliersTab.setText(str(self.supplier.getPersonEmail()))
        self.mainWindow.txtSupplierWebSuupliersTab.setText(str(self.supplier.getSupplierWeb()))

        self.mainWindow.txtAddressStreetSuppliersTab.setText(str(self.supplier.getAddressStreet()))
        if self.supplier.getAddresNumber() is not None:
            self.mainWindow.txtAddressNumberSupliersTab.setText(str(self.supplier.getAddresNumber()))
        else:
            self.mainWindow.txtAddressNumberSupliersTab.setText('')

        if self.supplier.getAddressFloor() is not None:
            self.mainWindow.txtAddressFloorSuppliersTab.setText(str(self.supplier.getAddressFloor()))
        else:
            self.mainWindow.txtAddressFloorSuppliersTab.setText('')

        if self.supplier.getAddressDpto() is not None:
            self.mainWindow.txtAddressDptoSuppliersTab.setText(self.supplier.getAddressDpto())
        else:
            self.mainWindow.txtAddressDptoSuppliersTab.setText('')

        if self.supplier.getPersonStatus() == 1:
            self.mainWindow.cbSupplierStatusSuppliersTab.setCurrentIndex(0)
        else:
            self.mainWindow.cbSupplierStatusSuppliersTab.setCurrentIndex(1)


    def validate(self):
        mensaje = ''
        if self.mainWindow.txtSupplierNameSuppliersTab.text() == '':
            mensaje = "Falta ingresar un Nombre"
        elif self.mainWindow.txtAddressStreetSuppliersTab.text() == '':
            mensaje = "Falta ingresar una Direccion"
        elif self.mainWindow.txtAddressNumberSupliersTab.text() == '':
            mensaje = "Falta ingresar un N° de Direccion"

        return mensaje


    def phoneLoadTable(self):
        self.initialPhoneList = self.phoneConnection.phoneListing(self.supplier)
        if len(self.initialPhoneList) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = TableModel(self.mainWindow, self.initialPhoneList, header)
            self.mainWindow.tvPhoneSuppliersTab.setModel(tableModel)
            self.mainWindow.tvPhoneSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.mainWindow.tvPhoneSuppliersTab.setColumnHidden(0, True)
            self.mainWindow.tvPhoneSuppliersTab.setColumnWidth(1, 36)
            self.mainWindow.tvPhoneSuppliersTab.setColumnWidth(2, 175)

            for r in range(0, len(self.initialPhoneList)):
                self.mainWindow.tvPhoneSuppliersTab.setRowHidden(r, False)


    def changeSelectedTableTel(self, selected, deselected):
        phoneList = selected.model().mylist
        self.selectedPhone = ()
        self.selectedPhone = phoneList[selected.row()]

        self.selectedPhoneRow = selected.row()
        self.mainWindow.btnPhoneSuppliersTab.setText(str(self.selectedPhone[2]))

        self.setTypePhone(str(self.selectedPhone[1]))
        self.mainWindow.btnCancelarTelefono_prov.setVisible(True)
        self.mainWindow.btnRestarTelefono_prov.setEnabled(True)
        self.mainWindow.tvPhoneSuppliersTab.setEnabled(False)

        self.mainWindow.btnSaveSuppliersTab.setEnabled(False)
        self.mainWindow.btnDeleteSuppliersTab.setEnabled(False)


    def updateTelefono(self):

        phoneList = []
        if self.mainWindow.tvPhoneSuppliersTab.model() != None and \
                        len(self.mainWindow.tvPhoneSuppliersTab.model().mylist) > 0:
            phoneList = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist).copy()

            estado = ''
            telNew = Phone()
            if len(phoneList) > 0:
                if len(self.initialPhoneList) > 0:

                    listTelInit = list(self.initialPhoneList)
                    parche = (phoneList[0][0], phoneList[0][1], str(phoneList[0][2]))
                    phoneList[0] = parche
                    #Recorre la lista de telefono inicial
                    for telInit in listTelInit:
                        #recorre la lista de telefonos nueva
                        for tel in phoneList:
                            telNew.setIdPersona(self.supplier.getIdPersona())
                            telNew.setIdTelefono(tel[0])
                            telNew.setTipo(tel[1])
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
                            self.phoneConnection.modificarTelefono(telNew)
                        elif estado == "INS":
                            self.phoneConnection.insertarTelefono(telNew)
                        elif estado == 'DEL':
                            self.phoneConnection.borrarTelefono(telNew)
                #Si la lista de telefono inicial es cero
                else:
                    #recorre la lista de telefonos nueva para agregarlos a todos
                    for telN in phoneList:
                        if telN[2] != '':
                            telNew = Phone()
                            telNew.setIdPersona(self.supplier.getIdPersona())
                            telNew.setIdTelefono(telN[0])
                            telNew.setTipo(telN[1])
                            telNew.setTelefono(telN[2])
                            self.phoneConnection.insertarTelefono(telNew)


    # def insertTelefono(self):
        
    #     header = ['Numero de telefono']
    #     newPhoneList = []
    #     model = TableModel(self.mainWindow, newPhoneList, header)
    #     newPhoneList = []
    #     tel = self.mainWindow.tvPhoneSuppliersTab.model()

    #     newPhoneList = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist).copy()

    #     if len(newPhoneList) > 0:
    #         self.phoneConnection.insertTelefonoInit(newPhoneList)


    def insertTelefono(self):
        # Define the header for the new model
        header = ['Numero de telefono']
    
        # Create a new instance of TableModel with an empty myList and the specified header
        model = TableModel(parent=self.mainWindow, myList=[], header=header)
    
        newPhoneList = []
    
        # Check if the model of tvPhoneSuppliersTab is not None
        if self.mainWindow.tvPhoneSuppliersTab.model():
            # Copy the existing myList data from tvPhoneSuppliersTab
            newPhoneList = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist).copy()
    
        # Update the model's myList with the copied data
        model.mylist = newPhoneList
    
        # Set the updated model to tvPhoneSuppliersTab
        self.mainWindow.tvPhoneSuppliersTab.setModel(model)
    
        # Check if there is data in newPhoneList
        if len(newPhoneList) > 0:
            self.phoneConnection.insertTelefonoInit(newPhoneList)




    def onClickCancelarTelefono(self):
        self.mainWindow.btnCancelarTelefono_prov.setVisible(False)
        self.mainWindow.btnPhoneSuppliersTab.setText('')

        self.mainWindow.btnRestarTelefono_prov.setEnabled(False)
        self.mainWindow.tvPhoneSuppliersTab.clearSelection()
        self.mainWindow.tvPhoneSuppliersTab.setEnabled(True)

        self.mainWindow.btnSaveSuppliersTab.setEnabled(True)
        self.mainWindow.btnDeleteSuppliersTab.setEnabled(True)


    def enableButtonAddPhone(self):
        phoneNumber = self.mainWindow.btnPhoneSuppliersTab.text()

        if phoneNumber.isdigit() == True:
            if self.mainWindow.btnCancelarTelefono_prov.isVisible() is True:
                self.updateTelefonoTabla()
            else:
                self.addPhoneTable()

            self.mainWindow.tvPhoneSuppliersTab.clearSelection()
            self.mainWindow.btnRestarTelefono_prov.setEnabled(False)
            self.mainWindow.btnCancelarTelefono_prov.setVisible(False)
            self.mainWindow.btnPhoneSuppliersTab.setText('')
            self.mainWindow.tvPhoneSuppliersTab.setEnabled(True)

            self.mainWindow.btnSaveSuppliersTab.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def enableButtonDeletePhone(self):
        listTabTel = []

        #tipoTel = str(self.getTypePhone())
        newPhoneList = []

        listTabTel = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.selectedPhone[0], self.selectedPhone[1], '']
        listTabTel[self.telefonoSelectedRow] = telDel
        tableTelModel = TableModel(self.mainWindow, listTabTel, header)
        self.mainWindow.tvPhoneSuppliersTab.setModel(tableTelModel)
        self.mainWindow.tvPhoneSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.mainWindow.tvPhoneSuppliersTab.setRowHidden(self.telefonoSelectedRow, True)

        self.mainWindow.btnCancelarTelefono_prov.setVisible(False)
        self.mainWindow.btnPhoneSuppliersTab.setText('')
        self.mainWindow.btnRestarTelefono_prov.setEnabled(False)
        self.mainWindow.tvPhoneSuppliersTab.setEnabled(True)

        self.mainWindow.btnSaveSuppliersTab.setEnabled(True)
        self.mainWindow.btnDeleteSuppliersTab.setEnabled(True)


    def enableButtonPhone(self):
        self.changeTypePhone(button='TEL')


    def enableButtonPhoneCell(self):
        self.changeTypePhone(button='CEL')


    def enableButtonPhoneFax(self):
        self.changeTypePhone(button='FAX')


    def changeTypePhone(self, button):

        if button == 'TEL':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(False)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(True)
        elif button == 'CEL':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(False)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(True)
        elif button == 'FAX':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(False)


    def setTypePhone(self, tipoTelefono):

        if tipoTelefono == 'TEL':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(False)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(True)
        elif tipoTelefono == 'CEL':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(False)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(True)
        elif tipoTelefono == 'FAX':
            self.mainWindow.btnPhoneSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneCellSuppliersTab.setEnabled(True)
            self.mainWindow.btnPhoneFaxSuppliersTab.setEnabled(False)


    def getTypePhone(self):

        if self.mainWindow.btnPhoneSuppliersTab.isEnabled() != True:
            return 'TEL'
        elif self.mainWindow.btnPhoneCellSuppliersTab.isEnabled() != True:
            return 'CEL'
        elif self.mainWindow.btnPhoneFaxSuppliersTab.isEnabled() != True:
            return 'FAX'


    def addPhoneTable(self):
        numTel = self.mainWindow.btnPhoneSuppliersTab.text()
        tipoTel = str(self.getTypePhone())

        modelListTelefono = self.mainWindow.tvPhoneSuppliersTab.model()
        header = ['ID', 'Tipo', 'Numero']

        if modelListTelefono is not None:
            listTabTel = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, numTel )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = TableModel(self.mainWindow, tupleTable , header)
                self.mainWindow.tvPhoneSuppliersTab.setModel(tableModel)
                self.mainWindow.tvPhoneSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, numTel )
            lista.append(tuplaTel)

            tableModel = TableModel(self.mainWindow, lista , header)
            self.mainWindow.tvPhoneSuppliersTab.setModel(tableModel)
            self.mainWindow.tvPhoneSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.mainWindow.tvPhoneSuppliersTab.setColumnHidden(0, True)
            self.mainWindow.tvPhoneSuppliersTab.setColumnWidth(1, 36)
            self.mainWindow.tvPhoneSuppliersTab.setColumnWidth(2, 175)


    def updateTelefonoTabla(self):
        listTabTel = []

        tipoTel = str(self.getTypePhone())
        newPhoneList = []
        prob = self.mainWindow.tvPhoneSuppliersTab.selectionModel()
        prob1 = self.mainWindow.tvPhoneSuppliersTab.model()
        listTabTel = list(self.mainWindow.tvPhoneSuppliersTab.model().mylist).copy()

        telUpd = (self.selectedPhone[0], tipoTel, int(self.mainWindow.btnPhoneSuppliersTab.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = TableModel(self.mainWindow, listTabTel , header)
        self.mainWindow.tvPhoneSuppliersTab.setModel(tableModel)
        self.mainWindow.tvPhoneSuppliersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)