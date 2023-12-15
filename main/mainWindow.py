#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from PyQt5.QtWidgets import QAction, QMainWindow
from PyQt5 import uic

from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication 


from main.suppliersTab import SuppliersTab
from main.customersTab import CustomersTab
from main.usersTab import UsersTab
from main.productsTab import ProductsTab
#from main.transactionsTab import TransactionsTab
#from main.paymentsTab import PaymentsTab
from connection.generalConnection import GeneralConnection
#from main.statisticsTab import StatisticsTab
#from main.stockNotificationWindow import StockNotificationWindow
#from main.accountsWindow import AccountsWindow
from PyQt5.Qt import QDesktopServices, QUrl

class MainWindow():

    def __init__(self, user):
        
       
        #Definiendo variables
        #self.user = user
        self.mainWindow = uic.loadUi('../view/mainWindow.ui')
        self.mainWindow.show()

        #self.setInterfaceUser()
        #self.mainWindow.maximumSize = self.mainWindow.size()
        self.mainWindow.setFixedSize(self.mainWindow.size())
        #self.notificationStock()
        self.mainWindow.twMenu.currentChanged.connect(self.changeTab)

    
        #self.mainWindow.actionSuppliersTab = QAction(self.mainWindow)
        #self.mainWindow.actionUsersTab = QAction(self.mainWindow)

        # self.transactionsTab = TransactionsTab(self.mainWindow)
        # self.paymentsTab = PaymentsTab(self.mainWindow)
        self.customersTab = CustomersTab(self.mainWindow)
        self.usersTab = UsersTab(self.mainWindow)
        self.suppliersTab = SuppliersTab(self.mainWindow)
        self.productsTab = ProductsTab(self.mainWindow)
       # self.statisticsTab = StatisticsTab(self.mainWindow)

#        self.mainWindow.actionListCliente.triggered.connect(self.openListCustomer)
#        self.mainWindow.actionListProveedor.triggered.connect(self.openListSupplier)
#        self.mainWindow.actionListStock.triggered.connect(self.openNotification)

#        self.mainWindow.actionTransactionsTab.triggered.connect(self.actionTransactionsTab)
 #       self.mainWindow.actionPaymentsTab.triggered.connect(self.actionPaymentsTab)
#        self.mainWindow.actionProductsTab.triggered.connect(self.actionProductsTab)
#        self.mainWindow.actionCustomersTab.triggered.connect(self.actionCustomersTab)
        #self.mainWindow.actionSuppliersTab.triggered.connect(self.actionSuppliersTab)
        #self.mainWindow.actionUsersTab.triggered.connect(self.actionUsersTab)
    #    self.mainWindow.actionEstaditicas.triggered.connect(self.actionStatistics)
     #   self.mainWindow.actionManual.triggered.connect(self.openManual)
        #self.mainWindow.actionReportarError.triggered.connect(self.openMail)

        #self.mainWindow.btnListProveedores_e.clicked.connect(self.openListSupplier)
        #self.mainWindow.btnListClientes_e.clicked.connect(self.openListCustomer)
        #self.mainWindow.btnListProductos_e.clicked.connect(self.openNotification)

        # if user.getUserType() == 'USUARIO':
        #     self.mainWindow.actionListCliente.setEnabled(False)
        #     self.mainWindow.actionListProveedor.setEnabled(False)
        #     self.mainWindow.actionListStock.setEnabled(False)

        #     self.mainWindow.actionUsersTab.setEnabled(False)
        #     self.mainWindow.actionEstaditicas.setEnabled(False)

    # def openListCustomer(self):
    #     self.accountsWindow = AccountsWindow(accountType='CLIENTE')

    # def openListSupplier(self):
    #     self.accountsWindow = AccountsWindow(accountType='PROVEEDOR')

    # def openMail(self):
    #     QDesktopServices.openUrl(QUrl("mailto:perico3372@mail.com?subject=Error&body=REPORTAR ERROR :"))


    def setInterfaceUser(self):

        if self.user.getUserType() == 'ADMINISTRADOR':
            self.mainWindow.twMenu.setTabEnabled(5, True)
            self.mainWindow.twMenu.setTabEnabled(6, True)
        else:
            self.mainWindow.twMenu.setTabEnabled(5, False)
            self.mainWindow.twMenu.setTabEnabled(6, False)

    # def notificationStock(self):
    #     generalConnection = GeneralConnection()

        # listProductsBelowSafetyStock = generalConnection.productStockListing()
        # self.mainWindow.btnNotification.setEnabled(False)
        # if len(listProductsBelowSafetyStock) > 0:
        #     self.mainWindow.btnNotification.setText(str(len(listProductsBelowSafetyStock)))
        #     self.mainWindow.btnNotification.setStyleSheet("border-top: 3px transparent;\nborder-bottom: 3px transparent;\nborder-right: 5px transparent;\nborder-left: 5px transparent;\ncolor: rgb(255, 0, 0);\nfont: 87 8pt Rockwell Extra Bold;")
        #     self.mainWindow.btnNotification.clicked.connect(self.openNotification)
        #     if self.user.getUserType() == 'ADMINISTRADOR':
        #         self.mainWindow.btnNotification.setEnabled(True)
        # else:
        #     self.mainWindow.btnNotification.setText("0")
        #     self.mainWindow.btnNotification.setStyleSheet("background-color: rgb(185, 185, 185);")

    # def openNotification(self):
    #     self.stockNotificationWindow = StockNotificationWindow()

    def changeTab(self):
#     #     #self.mainWindow.disconnect()
#     #     if self.mainWindow.twMenu.currentIndex() == 0:
#     #         #self.pestania.finish() transacciones
#     #         self.pestaniaTransaccion.cleanFields()
#     #     elif self.mainWindow.twMenu.currentIndex() == 1:
#     #         #self.pestania.finish() pagos
#     #         self.paymentsTab.cleanFields()
          #if self.mainWindow.twMenu.currentIndex() == 2:
#     #         #self.pestania.finish() producto
           #  self.productsTab.validateButtons('BORRAR')
          if self.mainWindow.twMenu.currentIndex() == 3:
#     #         #self.pestania.finish() cliente
               self.customersTab.validateButtons('BORRAR')
          #elif self.mainWindow.twMenu.currentIndex() == 4:
#              #self.pestania.finish() proveedor
              #self.suppliersTab.validateButtons('BORRAR')
          elif self.mainWindow.twMenu.currentIndex() == 5:
#     #         #self.pestania.finish() usuario
              self.usersTab.validateButtons('BORRAR')
#     #     elif self.mainWindow.twMenu.currentIndex() == 6:
#     #         #self.pestania.finish()
#     #         print('Estaditicas')

    def actionTransactionsTab(self):
        self.mainWindow.twMenu.setCurrentIndex(0)

    def actionPaymentsTab(self):
        self.mainWindow.twMenu.setCurrentIndex(1)

    def actionProductsTab(self):
        self.mainWindow.twMenu.setCurrentIndex(2)

    def actionCustomersTab(self):
        self.mainWindow.twMenu.setCurrentIndex(3)

    def actionSuppliersTab(self):
        self.mainWindow.twMenu.setCurrentIndex(4)

    def actionUsersTab(self):
        self.mainWindow.twMenu.setCurrentIndex(5)

    def actionStatistics(self):
        self.mainWindow.twMenu.setCurrentIndex(6)

# app = QApplication(sys.argv)
# mainWindow = MainWindow()
# sys.exit(app.exec_())