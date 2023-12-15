#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:30:34 2023

@author: pablo
"""

from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QMessageBox
import sys
from productConnection import ProductConnection 

class ProveedorSelector(QWidget):
    def __init__(self):
        super().__init__()

        # Crear una instancia de la clase ProductConnection
        self.products = ProductConnection()

        # Configurar la interfaz gráfica
        self.initUI()

    def initUI(self):
        # Crear widgets
        self.label = QLabel('Selecciona un proveedor:')
        # Obtener la lista de tuplas (ID, nombre)
        proveedores_tuplas = self.products.suppliersListing()
        self.comboBoxProveedores = QComboBox(self)
        
        # Asignar valores al QComboBox
        for proveedor_id, proveedor_nombre in proveedores_tuplas:
            self.comboBoxProveedores.addItem(proveedor_nombre, userData=proveedor_id)

        self.btnMostrarProveedor = QPushButton('Mostrar Proveedor', self)

        # Configurar el diseño
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.comboBoxProveedores)
        layout.addWidget(self.btnMostrarProveedor)

        # Configurar las señales y ranuras (slots)
        self.btnMostrarProveedor.clicked.connect(self.mostrarProveedor)

        # Establecer el diseño principal de la ventana
        self.setLayout(layout)

        # Configurar la ventana principal
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Selector de Proveedor')
        self.show()

    def mostrarProveedor(self):
        # Obtener el proveedor seleccionado
        proveedor_seleccionado = self.comboBoxProveedores.currentText()

        # Obtener el ID del proveedor seleccionado
        proveedor_id = self.comboBoxProveedores.currentData()

        # Mostrar información del proveedor seleccionado
        msg = f"Proveedor Seleccionado:\nNombre: {proveedor_seleccionado}\nID: {proveedor_id}"
        QMessageBox.information(self, 'Información del Proveedor', msg)

# Resto del código aquí ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    proveedor_selector = ProveedorSelector()
    sys.exit(app.exec_())
