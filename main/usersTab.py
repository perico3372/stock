import sys
sys.path.append('..')

from model.user import User
from connection.userConnection import UserConnection
from PyQt5.QtWidgets import QAbstractItemView
from model.table import TableModel
from model.address import Address
from connection.phoneConnection import PhoneConnection
from model.phone import Phone
from PyQt5.QtWidgets import QMessageBox, QDialog

class UsersTab():

    def __init__(self, mainWindows):
        self.mainWindows = mainWindows
        self.user = User()
        self.userConnection = UserConnection()
        self.phoneConnection = PhoneConnection()
        self.estado = ""
        self.address = Address()
        self.configInit()

    def configInit(self):

        #Configurando botones Generales
        self.mainWindows.btnAddUsersTab.clicked.connect(self.enableButtonAddUsersTab)
        self.mainWindows.btnSaveUsersTab.clicked.connect(self.enableButtonSaveUsersTab)
        self.mainWindows.btnDeleteUsersTab.clicked.connect(self.enableButtonDeleteUsersTab)
        self.mainWindows.btnUpdateUsersTab.clicked.connect(self.enableButtonUpdateUsersTab)

        #Configurando botones ABM telefono
        self.mainWindows.btnAddPhoneUsersTab.clicked.connect(self.enableButtonAddPhoneUsersTab)
        self.mainWindows.btnRestarTelefono_u.clicked.connect(self.onClickRestarTelefono)
        self.mainWindows.btnPhoneCancelUsersTab.clicked.connect(self.enableButtonCancelPhoneUsersTab)
        self.mainWindows.btnPhoneCancelUsersTab.setVisible(False)
        self.mainWindows.btnRestarTelefono_u.setEnabled(False)

        #configurando botones tipo telefono
        self.mainWindows.btnPhoneUsersTab.clicked.connect(self.onClickTelefono)
        self.mainWindows.btnPhoneCellUsersTab.clicked.connect(self.onClickCelular)
        self.mainWindows.btnFaxUsersTab.clicked.connect(self.onClickFax)

        self.mainWindows.txtFilterUserUsersTab.returnPressed.connect(self.search)

        #Seteando model y propieades de la tabla
        self.mainWindows.tvUserUsersTab.setSortingEnabled(True)
        self.mainWindows.tvUserUsersTab.setMouseTracking(True)
        self.mainWindows.tvUserUsersTab.setSelectionBehavior(QAbstractItemView.SelectRows)

        #Seteando proiedades de la tabla telefono
        self.mainWindows.tvPhoneUsersTab.setSortingEnabled(True)
        self.mainWindows.tvPhoneUsersTab.setMouseTracking(True)
        self.mainWindows.tvPhoneUsersTab.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.mainWindows.txtFilterUserUsersTab.setFocus(True)
        self.cleanFields()
        
        
        
    def finish(self):
        self.mainWindows.btnAddUsersTab.disconnect()
        self.mainWindows.btnDeleteUsersTab.disconnect()
        self.mainWindows.btnUpdateUsersTab.disconnect()
        self.mainWindows.btnSaveUsersTab.disconnect()

        self.mainWindows.btnPhoneCancelUsersTab.disconnect()
        self.mainWindows.btnAddPhoneUsersTab.disconnect()
        self.mainWindows.btnRestarTelefono_u.disconnect()

        self.mainWindows.btnPhoneCellUsersTab.disconnect()
        self.mainWindows.btnFaxUsersTab.disconnect()
        self.mainWindows.btnPhoneUsersTab.disconnect()

        self.mainWindows.tvPhoneUsersTab.disconnect()
        self.mainWindows.tvUserUsersTab.disconnect()

    def search(self):
        if self.mainWindows.txtFilterUserUsersTab.hasFocus() is True:
            self.loadTable()


    def enableButtonAddUsersTab(self):
        self.estado = 'AGREGAR'
        self.validateButtons(button='AGREGAR')

# ef enableButtonSaveCustomersTab(self):
#      validate = self.validate()

#      if validate != "":
#          print(validate)
#          alert = QDialog()
#          QMessageBox.information(alert,"ERROR", validate)
#      else:

#          self.customer.setPersonName(str(self.mainWindow.txtCustomerNameCustomersTab.text()))
#          self.customer.setPersonEmail(str(self.mainWindow.txtEmailCustomerCustomersTab.text()))

#          self.customer.setAddressStreet(str(self.mainWindow.txtAddressStreetCustomersTab.text()))   
#          if self.mainWindow.txtAddressDptoCustomersTab.text() != "":
#              self.customer.setAddressDpto(str(self.mainWindow.txtAddressDptoCustomersTab.text()))
#          else:
#              self.customer.setAddressDpto(0)
#          if self.mainWindow.txtAddressNumberCustomersTab.text() != "":
#              self.customer.setAddressNumber(int(self.mainWindow.txtAddressNumberCustomersTab.text()))
#          else:
#              self.customer.setAddressNumber("")
#          if self.mainWindow.txtAddressFloorCustomersTab.text() != "":
#              self.customer.setAddressFloor(int(self.mainWindow.txtAddressFloorCustomersTab.text()))
#          else:
#              self.customer.setAddressFloor(0)

#         # self.customer.setDireccion(self.address)

#          if self.mainWindow.cbCustomerStatusCustomersTab.currentText() == 'ACTIVO':
#              self.customer.setPersonStatus(1)
#          else:
#              self.customer.setPersonStatus(0)

#          self.validateButtons(button='GUARDAR')

#          if self.estado == 'AGREGAR':
#              self.addCustomers()
#              self.insertTelefono()
#          elif self.estado == 'MODIFICAR':
#              self.updateCustomers()
#              self.updateTelefono()

    def enableButtonUpdateCustomersTab(self):
        self.estado = 'MODIFICAR'
        self.validateButtons(button='MODIFICAR')



    def enableButtonSaveUsersTab(self):
        validar = self.validar()

        if validar != "":
            print(validar)
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", validar)
        else:
            
            self.user.setPersonName(str(self.mainWindows.txtPersonNameUsersTab.text()))
            self.user.setPersonEmail(str(self.mainWindows.txtUserEmailUsersTab.text()))
            self.user.setUserPasswd(str(self.mainWindows.txtUserPasswordUsersTab.text()))
            self.user.setUserName(str(self.mainWindows.txtUserNameUsersTab.text()))


            if self.mainWindows.cbUserTypeUsersTab.currentText() == 'user':
                self.user.setUserType("USUARIO")
            else:
                self.user.setUserType("ADMINISTRADOR")

            self.user.setAddressStreet(str(self.mainWindows.txtAddressStreetUsersTab.text()))
            if self.mainWindows.txtAddressDptoUsersTab.text() != "":
                self.user.setAddressDpto(str(self.mainWindows.txtAddressDptoUsersTab.text()))
            else:
                self.user.setAddressDpto("")
            if self.mainWindows.txtAddressNumberUsersTab.text() != "":
                self.user.setAddressNumber(int(self.mainWindows.txtAddressNumberUsersTab.text()))
            else:
                self.user.setAddressNumber("")
            if self.mainWindows.txtAddressFloorUsersTab.text() != "":
                self.user.setAddressFloor(int(self.mainWindows.txtAddressFloorUsersTab.text()))
            else:
                self.user.setAddressFloor("")

            self.user.setAddressStreet(self.address)

            self.validateButtons(button='GUARDAR')

            if self.estado == 'AGREGAR':
                self.addUsers()
                self.addPhoneUsersTab()
            elif self.estado == 'MODIFICAR':
                self.UpdateUsers()
                self.updatePhone()


    def enableButtonUpdateUsersTab(self):
        self.estado = 'MODIFICAR'
        self.validateButtons(button='MODIFICAR')


    def enableButtonDeleteUsersTab(self):
        if self.mainWindows.btnSaveUsersTab.isEnabled() != True:
            self.userConnection.borrarUsuario(self.user)
            self.loadTable()

        self.validateButtons(button='BORRAR')


    def loadTable(self):
        parameter = self.mainWindows.txtFilterUserUsersTab.text()
        typeParameter = ''

        if self.mainWindows.cbFilterUserUsersTab.currentText() == 'Nombre':
            typeParameter = 'ps.personName'
        if self.mainWindows.cbFilterUserUsersTab.currentText() == 'Usuario':
            typeParameter = 'u.userName'
        else:
            typeParameter = 'u.userType'

        userList = self.userConnection.userListing(typeParameter, parameter)
        if len(userList) > 0:

            header = ['ID', 'Nombre', 'Usuario', 'Tipo', 'Contraseña', 'Email','Direccion', 'N°', 'P', 'D',
                      'iddire', 'idpers']
            tableModel = TableModel(self.mainWindows.tvUserUsersTab, userList, header)
            self.mainWindows.tvUserUsersTab.setModel(tableModel)
            self.mainWindows.tvUserUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.mainWindows.tvUserUsersTab.setColumnHidden(0, True)
            self.mainWindows.tvUserUsersTab.setColumnWidth(1, 200)
            self.mainWindows.tvUserUsersTab.setColumnHidden(2, 200)
            self.mainWindows.tvUserUsersTab.setColumnWidth(3, 80)
            self.mainWindows.tvUserUsersTab.setColumnHidden(4, True)
            self.mainWindows.tvUserUsersTab.setColumnWidth(5, 100)
            self.mainWindows.tvUserUsersTab.setColumnWidth(6, 100)
            self.mainWindows.tvUserUsersTab.setColumnWidth(7, 100)
            self.mainWindows.tvUserUsersTab.setColumnHidden(8, 100)
            self.mainWindows.tvUserUsersTab.setColumnHidden(9, 100)
            self.mainWindows.tvUserUsersTab.setColumnHidden(10, True)
            self.mainWindows.tvUserUsersTab.setColumnHidden(11, True)
        else:
            self.mainWindows.tvUserUsersTab.setModel(None)


    def changeSelectedTable(self, selected, deselected):
        
      if hasattr(selected.model(), 'mylist') and selected.row() < len(selected.model().mylist):
        
        userList = selected.model().mylist
        selectedUser = userList[selected.row()]
        self.user = User()
        self.address = Address()
        self.user.setUserId(int(selectedUser[0]))
        self.user.setPersonName(str(selectedUser[1]))
        self.user.setUserName(str(selectedUser[2]))
        self.user.setUserType(str(selectedUser[3]))
        self.user.setUserPasswd(str(selectedUser[4]))
        self.user.setPersonEmail(str(selectedUser[5]))
        self.user.setAddressStreet(str(selectedUser[6]))
        if selectedUser[7] != None:
            self.user.setAddressNumber(int(selectedUser[7]))
        if selectedUser[8] != None:
            self.user.setAddressFloor(int(selectedUser[8]))
        if selectedUser[9] != None:
            self.user.setAddressDpto(selectedUser[9])
        self.user.setAddressId(selectedUser[10])
        self.user.setPersonId(selectedUser[11])
        self.mainWindows.tvUserUsersTab.setRowHeight(deselected.row(), 28)
        self.mainWindows.tvUserUsersTab.setRowHeight(selected.row(), 45)

        self.setFields()
        self.mainWindows.btnDeleteUsersTab.setEnabled(True)
        self.mainWindows.btnUpdateUsersTab.setEnabled(True)
        self.mainWindows.tvPhoneUsersTab.setModel(None)
        self.loadTableTelefono()


    def validateButtons(self, button):
        if button == 'AGREGAR' :
            self.mainWindows.wDatosUsuario.setEnabled(True)
            self.mainWindows.btnDeleteUsersTab.setEnabled(True)
            self.mainWindows.btnDeleteUsersTab.setText('CANCELAR')
            self.mainWindows.btnSaveUsersTab.setEnabled(True)
            self.mainWindows.btnUpdateUsersTab.setEnabled(False)
            self.mainWindows.btnAddUsersTab.setEnabled(False)
            self.mainWindows.tvUserUsersTab.setEnabled(False)
            self.cleanFields()

        elif button=='GUARDAR':
            self.mainWindows.btnUpdateUsersTab.setEnabled(False)
            self.mainWindows.btnAddUsersTab.setEnabled(True)
            self.mainWindows.btnSaveUsersTab.setEnabled(False)
            self.mainWindows.btnDeleteUsersTab.setText('BORRAR')
            self.mainWindows.btnDeleteUsersTab.setEnabled(False)
            self.mainWindows.tvUserUsersTab.setEnabled(True)
            self.mainWindows.wDatosUsuario.setEnabled(False)
            self.cleanFields()

        elif button == 'MODIFICAR':
            self.mainWindows.btnUpdateUsersTab.setEnabled(False)
            self.mainWindows.btnAddUsersTab.setEnabled(False)
            self.mainWindows.btnSaveUsersTab.setEnabled(True)
            self.mainWindows.btnDeleteUsersTab.setText('CANCELAR')
            self.mainWindows.btnDeleteUsersTab.setEnabled(True)
            self.mainWindows.tvUserUsersTab.setEnabled(False)
            self.mainWindows.wDatosUsuario.setEnabled(True)

        elif button=='BORRAR':
            self.mainWindows.btnUpdateUsersTab.setEnabled(False)
            self.mainWindows.btnAddUsersTab.setEnabled(True)
            self.mainWindows.btnSaveUsersTab.setEnabled(False)
            self.mainWindows.btnDeleteUsersTab.setText('BORRAR')
            self.mainWindows.btnDeleteUsersTab.setEnabled(False)
            self.mainWindows.tvUserUsersTab.setEnabled(True)
            self.mainWindows.wDatosUsuario.setEnabled(False)
            self.cleanFields()

    def addUsers(self):
        self.userConnection.addUsers(self.user)
        self.loadTable()

    def updateUsers(self):
        self.userConnection.updateUsers(self.user)
        self.loadTable()
        
        
        


    def cleanFields(self):
        self.mainWindows.txtPersonNameUsersTab.setText('')
        self.mainWindows.txtUserPasswordUsersTab.setText('')
        self.mainWindows.txtAddressStreetUsersTab.setText('')
        self.mainWindows.txtUserEmailUsersTab.setText('')
        self.mainWindows.txtUserNameUsersTab.setText('')
        self.mainWindows.cbUserTypeUsersTab.setCurrentIndex(0)
        self.mainWindows.txtAddressNumberUsersTab.setText('')
        self.mainWindows.txtAddressFloorUsersTab.setText('')
        self.mainWindows.txtAddressDptoUsersTab.setText('')
        self.mainWindows.tvPhoneUsersTab.setModel(None)
        self.mainWindows.txtFilterUserUsersTab.setText('')
        self.mainWindows.tvUserUsersTab.setModel(None)

        self.mainWindows.txtFilterUserUsersTab.setFocus(True)

    def setFields(self):
        self.mainWindows.txtPersonNameUsersTab.setText(str(self.user.getPersonName()))
        self.mainWindows.txtUserPasswordUsersTab.setText(str(self.user.getUserPasswd()))
        self.mainWindows.txtUserEmailUsersTab.setText(str(self.user.getPersonEmail()))
        self.mainWindows.txtUserNameUsersTab.setText(str(self.user.getUserName()))
        if self.user.getUserType() == 'ADMINISTRADOR':
            self.mainWindows.cbUserTypeUsersTab.setCurrentIndex(1)
        elif self.user.getUserType() == 'USUARIO':
            self.mainWindows.cbUserTypeUsersTab.setCurrentIndex(0)

        self.mainWindows.txtAddressStreetUsersTab.setText(str(self.user.getAddressStreet()))
        if self.user.getAddressNumber() != None:
            self.mainWindows.txtAddressNumberUsersTab.setText(str(self.user.getAddresNumber()))
        else:
            self.mainWindows.txtAddressNumberUsersTab.setText('')
        if self.user.getAddressFloor() != None:
            self.mainWindows.txtAddressFloorUsersTab.setText(str(self.getAddressFloor()))
        else:
            self.mainWindows.txtAddressFloorUsersTab.setText('')
        if self.user.getAddressDpto() != None:
            self.mainWindows.txtAddressDptoUsersTab.setText(self.user.getAddressDpto())
        else:
            self.mainWindows.txtAddressDptoUsersTab.setText('')


    def validar(self):
        mensaje = ""

        if self.mainWindows.txtPersonNameUsersTab.text() == '':
            mensaje = "Falta ingresar un Nombre."
        elif self.mainWindows.txtAddressStreetUsersTab.text() == '':
            mensaje = "Falta ingresar la Direccion"
        elif self.mainWindows.txtUserNameUsersTab.text() == '':
            mensaje = "Falta ingresar el nombre de usuario"
        elif self.mainWindows.txtUserPasswordUsersTab.text() == '':
            mensaje = "Falta ingresa la contraseña."

        return mensaje


    def loadTableTelefono(self):
        self.initialPhoneList = self.phoneConnection.selectTelefono(self.user)
        if len(self.initialPhoneList) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = TableModel(self.mainWindows, self.initialPhoneList, header)
            self.mainWindows.tvPhoneUsersTab.setModel(tableModel)
            self.mainWindows.tvPhoneUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.mainWindows.tvPhoneUsersTab.setColumnHidden(0, True)
            self.mainWindows.tvPhoneUsersTab.setColumnWidth(1, 36)
            self.mainWindows.tvPhoneUsersTab.setColumnWidth(2, 175)

            for r in range(0, len(self.initialPhoneList)):
                self.mainWindows.tvPhoneUsersTab.setRowHidden(r, False)



    def changeSelectedTableTel(self, selected, deselected):
        listTelefonos = selected.model().mylist
        self.telefonoSelected = ()
        self.telefonoSelected = listTelefonos[selected.row()]

        self.telefonoSelectedRow = selected.row()
        self.mainWindows.txtAddPhoneUsersTab.setText(str(self.telefonoSelected[2]))

        self.setTipoTelefono(str(self.telefonoSelected[1]))
        self.mainWindows.btnPhoneCancelUsersTab.setVisible(True)
        self.mainWindows.btnRestarTelefono_u.setEnabled(True)
        self.mainWindows.tvPhoneUsersTab.setEnabled(False)

        self.mainWindows.btnSaveUsersTab.setEnabled(False)
        self.mainWindows.btnDeleteUsersTab.setEnabled(False)

    def updatePhone(self):

        PhoneList = []
        phoneList = list(self.mainWindows.tvPhoneUsersTab.model().mylist).copy()

        estado = ''
        newPhone = Phone()
        if len(PhoneList) > 0:
            if len(self.phoneListsInit) > 0:

                listTelInit = list(self.phoneListsInit)
                parche = (phoneList[0][0], phoneList[0][1], str(phoneList[0][2]))
                phoneList[0] = parche
                #Recorre la lista de telefono inicial
                for telInit in listTelInit:
                    #recorre la lista de telefonos nueva
                    for tel in phoneList:
                        newPhone.setIdPersona(self.user.getIdPersona())
                        newPhone.setIdTelefono(tel[0])
                        newPhone.setTipo(tel[1])
                        if tel[2] == "":
                            estado = 'DEL'
                            break
                        else:
                            newPhone.setTelefono(tel[2])

                        if tel[0] == 0:
                            estado = 'INS'
                            break

                        if telInit[0] == tel[0]:
                            if telInit[1] != tel[1] or telInit[2] != tel[2]:
                                estado = 'UPD'
                                break

                    if estado == 'UPD':
                        self.phoneConnection.modificarTelefono(newPhone)
                    elif estado == "INS":
                        self.phoneConnection.insertarTelefono(newPhone)
                    elif estado == 'DEL':
                        self.phoneConnection.borrarTelefono(newPhone)
            #Si la lista de telefono inicial es cero
            else:
                #recorre la lista de telefonos nueva para agregarlos a todos
                for telN in phoneList:
                    if telN[2] != '':
                        newPhone = Phone()
                        newPhone.setIdPersona(self.user.getIdPersona())
                        newPhone.setIdTelefono(telN[0])
                        newPhone.setTipo(telN[1])
                        newPhone.setTelefono(telN[2])
                        self.phoneConnection.insertarTelefono(newPhone)



    # def addPhone(self):

    #     phoneListsNew = []
    #     tel = self.mainWindows.tvPhoneUsersTab.model()

    #     listTelefonosNew = list(self.mainWindows.tvPhoneUsersTab.model().mylist).copy()

    #     if len(listTelefonosNew) > 0:
    #         self.phoneConnection.insertTelefonoInit(listTelefonosNew)



    def addPhoneUsersTab(self):
        # Verificar si el modelo no es None antes de acceder a mylist
        modelListTelefono = self.mainWindows.tvPhoneUsersTab.model()
        if modelListTelefono is not None:
            # Ahora puedes acceder a mylist sin causar un AttributeError
            listTabTel = list(modelListTelefono.mylist).copy()
            # Resto del código...
        else:
            # Manejar el caso en el que el modelo es None
            print("El modelo de la tabla de teléfonos es None")
    


    def enableButtonCancelPhoneUsersTab(self):
        self.mainWindows.btnPhoneCancelUsersTab.setVisible(False)
        self.mainWindows.txtAddPhoneUsersTab.setText('')

        self.mainWindows.btnRestarTelefono_u.setEnabled(False)
        self.mainWindows.tvPhoneUsersTab.clearSelection()
        self.mainWindows.tvPhoneUsersTab.setEnabled(True)

        self.mainWindows.btnSaveUsersTab.setEnabled(True)
        self.mainWindows.btnDeleteUsersTab.setEnabled(True)

    def enableButtonAddPhoneUsersTab(self):
        numTelefono = self.mainWindows.txtAddPhoneUsersTab.text()

        if numTelefono.isdigit() == True:
            if self.mainWindows.btnPhoneCancelUsersTab.isVisible() is True:
                self.updatePhoneTable()
            else:
                self.addPhoneTable()

            self.mainWindows.tvPhoneUsersTab.clearSelection()
            self.mainWindows.btnRestarTelefono_u.setEnabled(False)
            self.mainWindows.btnPhoneCancelUsersTab.setVisible(False)
            self.mainWindows.txtAddPhoneUsersTab.setText('')
            self.mainWindows.tvPhoneUsersTab.setEnabled(True)

            self.mainWindows.btnSaveUsersTab.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def onClickRestarTelefono(self):
        listTabTel = []
        tipoTel = str(self.getPhoneType())
        listTelefonosNew = []

        listTabTel = list(self.mainWindows.tvPhoneUsersTab.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.telefonoSelected[0], self.telefonoSelected[1], '']
        listTabTel[self.telefonoSelectedRow] = telDel
        tableTelModel = TableModel(self.mainWindows, listTabTel, header)
        self.mainWindows.tvPhoneUsersTab.setModel(tableTelModel)
        self.mainWindows.tvPhoneUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.mainWindows.tvPhoneUsersTab.setRowHidden(self.telefonoSelectedRow, True)

        self.mainWindows.btnPhoneCancelUsersTab.setVisible(False)
        self.mainWindows.txtAddPhoneUsersTab.setText('')
        self.mainWindows.btnRestarTelefono_u.setEnabled(False)
        self.mainWindows.tvPhoneUsersTab.setEnabled(True)

        self.mainWindows.btnSaveUsersTab.setEnabled(True)
        self.mainWindows.btnDeleteUsersTab.setEnabled(True)

    def onClickTelefono(self):
        self.changePhoneType(button='TEL')

    def onClickCelular(self):
        self.changePhoneType(button='CEL')

    def onClickFax(self):
        self.changePhoneType(button='FAX')

    def changePhoneType(self, button):

        if button == 'TEL':
            self.mainWindows.btnPhoneUsersTab.setEnabled(False)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(True)
            self.mainWindows.btnFaxUsersTab.setEnabled(True)
        elif button == 'CEL':
            self.mainWindows.btnPhoneUsersTab.setEnabled(True)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(False)
            self.mainWindows.btnFaxUsersTab.setEnabled(True)
        elif button == 'FAX':
            self.mainWindows.btnPhoneUsersTab.setEnabled(True)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(True)
            self.mainWindows.btnFaxUsersTab.setEnabled(False)


    def setTipoTelefono(self, tipoTelefono):

        if tipoTelefono == 'TEL':
            self.mainWindows.btnPhoneUsersTab.setEnabled(False)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(True)
            self.mainWindows.btnFaxUsersTab.setEnabled(True)
        elif tipoTelefono == 'CEL':
            self.mainWindows.btnPhoneUsersTab.setEnabled(True)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(False)
            self.mainWindows.btnFaxUsersTab.setEnabled(True)
        elif tipoTelefono == 'FAX':
            self.mainWindows.btnPhoneUsersTab.setEnabled(True)
            self.mainWindows.btnPhoneCellUsersTab.setEnabled(True)
            self.mainWindows.btnFaxUsersTab.setEnabled(False)

    def getPhoneType(self):

        if self.mainWindows.btnPhoneUsersTab.isEnabled() != True:
            return 'TEL'
        elif self.mainWindows.btnPhoneCellUsersTab.isEnabled() != True:
            return 'CEL'
        elif self.mainWindows.btnFaxUsersTab.isEnabled() != True:
            return 'FAX'


    def addPhoneTable(self):
        numTel = self.mainWindows.txtAddPhoneUsersTab.text()
        tipoTel = str(self.getPhoneType())

        modelListTelefono = self.mainWindows.tvPhoneUsersTab.model()
        header = ['ID', 'Tipo', 'Numero']

        if modelListTelefono is not None:
            listTabTel = list(self.mainWindows.tvPhoneUsersTab.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, numTel )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = TableModel(self.mainWindows, tupleTable , header)
                self.mainWindows.tvPhoneUsersTab.setModel(tableModel)
                self.mainWindows.tvPhoneUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, numTel )
            lista.append(tuplaTel)

            tableModel = TableModel(self.mainWindows, lista , header)
            self.mainWindows.tvPhoneUsersTab.setModel(tableModel)
            self.mainWindows.tvPhoneUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.mainWindows.tvPhoneUsersTab.setColumnHidden(0, True)
            self.mainWindows.tvPhoneUsersTab.setColumnWidth(1, 36)
            self.mainWindows.tvPhoneUsersTab.setColumnWidth(2, 175)


    def updatePhoneTable(self):
        listTabTel = []
        tipoTel = str(self.getPhoneType())
        listTelefonosNew = []
        prob = self.mainWindows.tvPhoneUsersTab.selectionModel()
        prob1 = self.mainWindows.tvPhoneUsersTab.model()
        listTabTel = list(self.mainWindows.tvPhoneUsersTab.model().mylist).copy()

        telUpd = (self.telefonoSelected[0], tipoTel, int(self.mainWindows.txtAddPhoneUsersTab.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = TableModel(self.mainWindows, listTabTel , header)
        self.mainWindows.tvPhoneUsersTab.setModel(tableModel)
        self.mainWindows.tvPhoneUsersTab.selectionModel().currentChanged.connect(self.changeSelectedTableTel)