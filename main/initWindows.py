#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:41:10 2023

@author: pablo
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from connection.userConnection import UserConnection
from model.user import User
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication 
from PyQt5 import uic




class InitWindow():

    def __init__(self):

        self.initWindows = uic.loadUi('../view/login.ui')
        self.userConnection = UserConnection()
        #self.initWindows.btnIniciar.clicked.connect(self.onClickValidarUsuario)
        self.initWindows.btnSalir.clicked.connect(self.onClickSalir)
        self.user = User()
        self.initWindows.txtUsuario.setFocus(True)
        self.initWindows.show()


    def onClickValidarUsuario(self):

        self.user = User()
        self.user.setUserName(self.initWindows.txtUsuario.text())
        self.user.setUserPasswd(self.initWindows.txtPass.text())
        value = ''
        if self.user.getUserName() != '' and self.user.getUserPasswd() != '':
            value  = self.userConnection.connectionUserValidateUser(user=self.user)
            if len(value) != 0:
                self.user.setUserName(value[0][0])
                self.user.setUserType(value[0][1])
                self.initWindows.txtPass.setText('')
                self.initWindows.txtUsuario.setText('')
                return self.user
            else:
                self.initWindows.lblError.setText('LA CONTRASEÑA O USUARIO NO COINCIDEN')
                self.initWindows.txtPass.setText('')
                alert = QDialog()
                QMessageBox.information(alert,"ERROR", 'LA CONTRASEÑA O USUARIO NO COINCIDEN')
        else:
            print('Falta completar algun campo')
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", 'Falta completar algun campo')



    def onClickSalir(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea salir ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.initWindows.close()


