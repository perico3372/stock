#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 22:15:24 2023

@author: pablo
"""

# init.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.userConnection import UserConnection
from model.user import User
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication 

from main.mainWindow import MainWindow 


class Init():

    def __init__(self):

        self.init = uic.loadUi('../view/login.ui')
        self.userConnection = UserConnection()
        self.init.btnIniciar.clicked.connect(self.onClickValidarUsuario)
        self.init.btnSalir.clicked.connect(self.onClickSalir)
        self.user = User()
        self.init.txtUsuario.setFocus(True)
        self.init.show()

    def onClickValidarUsuario(self):

        self.user = User()
        self.user.setUserName(self.init.txtUsuario.text())
        self.user.setUserPasswd(self.init.txtPass.text())
        value = ''
        if self.user.getUserName() != '' and self.user.getUserPasswd() != '':
            value = self.userConnection.connectionUserValidateUser(user=self.user)
            if len(value) != 0:
                self.user.setUserName(value[0][0])
                self.user.setUserType(value[0][1])
                self.init.txtPass.setText('')
                self.init.txtUsuario.setText('')
                print(f'User {self.user.getUserName()} successfully authenticated')
                self.init.hide()
                #self.init.close()
                # Open the main window after successful login
                #main_window = MainWindow(self.user)
                
                main_window = MainWindow(self.user)
                main_window.show()
                return self.user
            else:
                self.init.lblError.setText('LA CONTRASEÑA O USUARIO NO COINCIDEN')
                self.init.txtPass.setText('')
                alert = QDialog()
                QMessageBox.information(alert, "ERROR", 'LA CONTRASEÑA O USUARIO NO COINCIDEN')
        else:
            print('Falta completar algún campo')
            alert = QDialog()
            QMessageBox.information(alert, "ERROR", 'Falta completar algún campo')

    def onClickSalir(self):
        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿Desea salir?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            print(f'Exiting application. User: {self.user.getUserName()}')
            self.init.close()

app = QApplication(sys.argv)
init = Init()
sys.exit(app.exec_())