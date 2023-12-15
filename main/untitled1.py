#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:51:37 2023

@author: pablo
"""

import sys
#sys.path.append('..')

from PyQt5.QtWidgets import QApplication

from mainWindow import MainWindow
from initWindows import InitWindow
from PyQt5.QtWidgets import QMessageBox, QDialog

class windowMain():

    def __init__(self):
        #self.Principal = Principal()

        self.initialize = InitWindow()
        self.initialize.initWindows.btnIniciar.clicked.connect(self.comprobarUsuario)


    def comprobarUsuario(self):
        user = self.initialize.onClickValidarUsuario()
        if user != None:
            self.main = MainWindow(user=user)
            self.initialize.initWindows.close()
            self.main.mainWindow.lblNombreUsuario.setText(user.getUserName())
            self.main.mainWindow.actionCerrarSesion.triggered.connect(self.cerrarSesion)
            self.main.mainWindow.actionSalir.triggered.connect(self.salir)


    def cerrarSesion(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea cerrar sesion ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            #self.initialize.initWindows.show()
            self.initialize = InitWindow()
            self.initialize.initWindows.btnIniciar.clicked.connect(self.comprobarUsuario)
            self.main.mainWindow.close()


    def salir(self):
        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea salir ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.main.mainWindow.close()


app = QApplication(sys.argv)
init = windowMain()
sys.exit(app.exec_())
