#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:39:38 2023

@author: pablo
"""
import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from productConnection import ProductConnection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Crear una instancia de la clase ProductConnection
        product_connection = ProductConnection()

        # Obtener los combo boxes con la lista de proveedores, marcas y categorías
        combo_box_suppliers = product_connection.suppliersListing()
        combo_box_brands = product_connection.brandsListing()
        combo_box_categories = product_connection.categoriesListing()

        # Crear etiquetas para mostrar la selección actual de cada combo box
        label_supplier = QLabel("Proveedor seleccionado:")
        label_brand = QLabel("Marca seleccionada:")
        label_category = QLabel("Categoría seleccionada:")

        # Conectar las señales del combo box a las funciones de actualización
        combo_box_suppliers.currentIndexChanged.connect(lambda: self.update_label(label_supplier, combo_box_suppliers))
        combo_box_brands.currentIndexChanged.connect(lambda: self.update_label(label_brand, combo_box_brands))
        combo_box_categories.currentIndexChanged.connect(lambda: self.update_label(label_category, combo_box_categories))

        # Crear un diseño vertical y agregar widgets
        layout = QVBoxLayout()
        layout.addWidget(combo_box_suppliers)
        layout.addWidget(label_supplier)
        layout.addWidget(combo_box_brands)
        layout.addWidget(label_brand)
        layout.addWidget(combo_box_categories)
        layout.addWidget(label_category)

        # Configurar el diseño principal de la ventana
        self.setLayout(layout)
        self.setWindowTitle("Ejemplo de Combo Box")
        self.setGeometry(100, 100, 400, 300)

    def update_label(self, label, combo_box):
        # Actualizar la etiqueta con la selección actual del combo box
        selected_text = combo_box.currentText()
        label.setText(f"{label.text().split()[0]}: {selected_text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
