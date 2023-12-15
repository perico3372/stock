import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.customer import Customer
from model.supplier import Supplier
from model.product import Product
import datetime

class TransactionConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.customer = Customer()
        self.supplier = Supplier()


    def listSupplier(self, typeParameter, parameter):
        query = """
                    SELECT s.supplierId , s.supplierDescription, p.namePerson, p.emailPerson
                    FROM suppliers s, persons p
                    WHERE p.personId = s.persons_personId and s.suplierStatus = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listsuppliers = self.databaseConnection.cursor.fetchall()

        self.databaseConnection.closeConnection()

        return listsuppliers

    def listCustomer(self, typeParameter, parameter):
        query = """
                    SELECT c.customerId, ps.namePerson, ps.emailPerson
                    FROM customers c, persons ps
                    WHERE ps.personId = c.persons_personId and c.customerStatus = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listClientes = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listClientes

    def productsListing(self, typeParameter, parameter, parameterTransaccion):
        query = """
                    SELECT pr.productId, pr.productName, pr.ProductDescription, pr.quantity, 
                    AST(TRUNCATE(pr.purchasePrice, 2) AS CHAR), CAST(TRUNCATE(pr.salesPrice, 2) AS CHAR), b.brandName
                    FROM products pr, brands b
                    WHERE pr.brands_brandId = b.brandId and """ +typeParameter+ """ LIKE %s
                """
        if parameterTransaccion == 'VNT':
            query += " and pr.productStatus = 1 and pr.quantity > 0"

        param = parameter + '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, param)
        productsList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return productsList

    def loadPurchaseTransaction(self, transactionsList, supplier, status):
        hoy = datetime.datetime.now().date()

        self.databaseConnection.openConnection()

        queryTipoMovimiento = """
                                INSERT INTO transactionType (transactionType, suppliers_supplierId)
                                VALUES ('compra', %s)
                              """
        valuesTipoMovimiento = supplier.getSupplierId()

        self.databaseConnection.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.databaseConnection.db.commit()
        transactionTypeId = self.databaseConnection.cursor.lastrowid
        cantRowAffect = self.databaseConnection.cursor.rowcount


        transactionQuery = """
                            INSERT INTO transactions (transactionDate, transactionType_transactionTypeId, transactionStatus)
                            VALUES ( %s , %s, %s)
                          """
        transactionValues = (hoy, transactionTypeId, status)

        self.databaseConnection.cursor.execute(transactionQuery, transactionValues)
        self.databaseConnection.db.commit()
        transactionsId = self.databaseConnection.cursor.lastrowid
        cantRowAffect = self.databaseConnection.cursor.rowcount


        transactionDetailQuery = """
                            INSERT INTO transactionDetail (quantity, unitPrice, products_productId,
                                transactions_transactionId)
                            VALUES (%s, %s , %s, %s)
                           """
        for transactionDetail in transactionsList:
            transactionDetailValues = (transactionDetail[1], transactionDetail[5], transactionDetail[2], transactionsId)
            self.databaseConnection.cursor.execute(transactionDetailQuery, transactionDetailValues)
            self.databaseConnection.db.commit()
            lastId = self.databaseConnection.cursor.lastrowid
            cantRowAffect = self.databaseConnection.cursor.rowcount
            product = Product()
            product.setProductId(int(transactionDetail[2]))
            product.setProductQuantity(int(transactionDetail[1]))
            self.modificarStock('CMP', product)

        self.databaseConnection.closeConnection()
        return transactionsId

    def loadSalesTransanctions(self: object, transactionsList, cliente, status):
        today = datetime.datetime.now().date()

        self.databaseConnection.openConnection()

        queryTipoMovimiento = """
                                INSERT INTO transactionType (transactionType, customers_customerId)
                                VALUES ('venta', %s)
                              """
        valuesTipoMovimiento = cliente.getIdCliente()

        self.databaseConnection.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.databaseConnection.db.commit()
        transactionTypeId = self.databaseConnection.cursor.lastrowid
        cantRowAffect = self.databaseConnection.cursor.rowcount


        transactionQuery = """
                            INSERT INTO transactions (transactionDate, transactionType_idtransactionType, trnsactionStatus)
                            VALUES ( %s , %s, %s);
                          """
        transactionValues = (today, transactionTypeId, status)

        self.databaseConnection.cursor.execute(transactionQuery, transactionValues)
        self.databaseConnection.db.commit()
        transactionsId = self.databaseConnection.cursor.lastrowid
        cantRowAffect = self.databaseConnection.cursor.rowcount


        transactionDetailQuery = """
                            INSERT INTO transactionDetail (quantity, unitPrice, products_productId,
                                transactions_transactionId)
                            VALUES (%s, %s , %s, %s)
                           """
        for transactionDetail in transactionsList:
            transactionDetailValues = (transactionDetail[1], transactionDetail[5], transactionDetail[2], transactionsId)
            self.databaseConnection.cursor.execute(transactionDetailQuery, transactionDetailValues)
            self.databaseConnection.db.commit()
            lastId = self.databaseConnection.cursor.lastrowid
            cantRowAffect = self.databaseConnection.cursor.rowcount

            product = Product()
            product.setProductId(int(transactionDetail[2]))
            product.setProductQuantity(int(transactionDetail[1]))
            self.modificarStock(tipoT='VNT', product=product)

        self.databaseConnection.closeConnection()

        return transactionsId

    def UpdateStock(self, tipoT, product):
        query = """
                    SELECT quantity
                    FROM products
                    WHERE productId = %s
                """
        values = product.getProductId()
        #self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        quantity = 0
        InitialQuantity = int(self.databaseConnection.cursor.fetchall()[0][0])
        #self.databaseConnection.closeConnection()
        if tipoT == 'VNT':
            quantity = InitialQuantity - product.getProductQuantity()
        else:
            quantity = InitialQuantity + product.getProductQuantity()

        UpdateProductsQuery = """
                                UPDATE products
                                SET quantity = %s
                                WHERE productId = %s
                              """
        valuesUpdateProducto = (quantity, product.getProductId())
        #self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(UpdateProductsQuery, valuesUpdateProducto)
        self.databaseConnection.db.commit()
        #self.databaseConnection.closeConnection()