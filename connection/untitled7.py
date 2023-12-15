#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:49:34 2023

@author: pablo
"""

# main.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox
from otro_modulo import Proveedor

class ProductsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Crear QComboBox editable
        self.comboBoxProveedor = QComboBox(self)
        self.comboBoxProveedor.setEditable(True)

        # Conectar señal a método
        self.comboBoxProveedor.editTextChanged.connect(self.actualizar_combobox)

        # Inicializar ComboBox
        self.actualizar_combobox()

        # Diseño básico para mostrar el QComboBox
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Proveedores:"))
        layout.addWidget(self.comboBoxProveedor)

    def actualizar_combobox(self):
        # Obtener lista de proveedores desde la clase Proveedor
        proveedores = Proveedor.obtener_proveedores()

        # Limpiar y agregar elementos al ComboBox
        self.comboBoxProveedor.clear()
        self.comboBoxProveedor.addItems(proveedores)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = ProductsTab()
    mainWin.show()
    app.exec_()
