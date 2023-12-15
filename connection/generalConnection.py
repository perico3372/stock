

import sys
sys.path.append('..')


from connection.databaseConnection import DatabaseConnection
from model.product import Product
from model.supplier import Supplier
from model.customer import Customer

class GeneralConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.product = Product()
        supplier = Supplier()
        customer = Customer()

    def productStockListing(self):

        query = """
                   SELECT productId, nameProduct, quantity, minimumQuantity
                   FROM products
                   WHERE productStatus = 1 and quantity BETWEEN 0 and minimumQuantity
               """

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        productList = self.databaseConnection.cursor.fetchall()

        self.databaseConnection.closeConnection()

        return productList

    def changeStutusProduct(self, product):
        query ="""
                    UPDATE products
                    SET status = '0'
                    WHERE productId = %s
               """
        values = product.getProductId()

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def monthlySalesListing(self):
        query = """
                    SELECT t.transactionDate , CAST(SUM(dm.cantidad) AS CHAR)
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tm.customers_customerId and
                        t.transactionType_idtransactionType = tm.transactionTypeId and
                        t.transactionId = dm.transactions_transactionId
                    GROUP BY month(t.transactionDate)
                """
        self.databaseConnection.openConnection()

        self.databaseConnection.cursor.execute(query)
        monthlySalesList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return monthlySalesList

    def monthlyPurchasesListing(self):
        query = """
                    SELECT t.transactionDate , CAST(SUM(tD.quantity) AS CHAR)
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tT.customers_customerId and
                        t.transactionType_idtransactionType = tm.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId
                    GROUP BY month(t.transactionDate)
                """

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        monthlyPurchaseList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return monthlyPurchaseList


    def annualSalesListing(self):
        query = """
                    SELECT t.transactionDate , CAST(SUM(tD.quantity) AS CHAR)
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tm.customers_customerId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId
                    GROUP BY year(t.transactionDate)
                """
        self.databaseConnection.openConnection()

        self.databaseConnection.cursor.execute(query)

        annualSalesList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return annualSalesList

    def annualPurchasesListing(self):
        query = """
                    SELECT t.transactionDate , CAST(SUM(tD.quantity) AS CHAR)
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tT.customers_customerId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId
                    GROUP BY year(t.transactionDate)
                """

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        annualSalesList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return annualSalesList


    def salesListing(self, interval, initialDate, finalDate):
        query = """
                    SELECT CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR)) AS fecha,
                           CAST(SUM(dm.cantidad) AS CHAR) as cantidad
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tm.customers_customerId and
                          t.transactionType_idtransactionType = tm.transactionTypeId and
                          t.transactionId = dm.transactions_transactionId and
						  t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (initialDate, finalDate)


        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        salesList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return salesList

    def purchaseListing(self, interval, initialDate, finalDate):
        query = """
                    SELECT CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR)) AS fecha,
                           CAST(SUM(tD.quantity) AS CHAR) as cantidad
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tm.customers_customerId and
                          m.transactionType_idtransactionType = tm.transactionTypeId and
                          m.transactionId = dm.transactions_transactionId and
                          m.transactionId = dm.transactions_transactionId and
						  t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        purchaseList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return purchaseList

    def supplierListing(self, parameter):
        query ="""
                    SELECT s.supplierId, s.supplierDescription, p.namePerson
                    FROM suppliers s, persons p
                    WHERE p.idpersonas = s.persons_personId and
                    s.supplierDescription LIKE %s
               """
        param = parameter+ '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        supplierList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return supplierList

    def customerListing(self, parameter):
        query = """
                    SELECT c.customerId, c.lastName, p.namePerson
                    FROM customers c, persons p
                    WHERE p.personId = c.persons_personId and
                            cli.lastName LIKE %s
                """
        param = parameter+ '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        customerList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return customerList


    def suppliersPaymentsListing(self, supplier, interval, initialDate, finalDate):

        selectDate = ''
        if interval == 'day':
            selectDate = "p.paymentDate"
        else:
            selectDate = """CONCAT(CAST(year(p.paymentDate) AS CHAR) ,"-", CAST("""+interval+"""(p.paymentDate) AS CHAR))"""
        query = """
                    SELECT """+ selectDate +""" AS fecha , SUM(p.paymentAmount), tm.transactionType
                    FROM suppliers s, payments p, transactionType tT
                    WHERE tm.customers_customerId = s.supplierId and
                        p.transactionType_idtransactionType = tm.transactionTypeId and
                        s.supplierId = %s and
	                    p.paymentDate between %s and %s
                    GROUP BY """+ interval +"""(p.paymentDate)
					ORDER BY p.paymentDate
                """
        values = (supplier.getIdProveedor(), initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        paymentsList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return paymentsList

    def suppliersTransactionsListing(self, supplier, interval, initialDate, finalDate):

        selectDate = ''
        if interval == 'day':
            selectDate = "t.transactionDate"
        else:
            selectDate = """CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR))"""
        query = """
                    SELECT """+ selectDate +""" AS fecha,
                    SUM(tD.precio_unitario * dm.cantidad) as monto, tm.transactionType
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tm.customers_customerId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.transactionId = dm.transactions_transactionId and t.transactionStatus = 0 and
                        s.supplierId = % s and
	                    t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (supplier.getIdProveedor(), initialDate, finalDate)

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listTransactions = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listTransactions

    def customerPaymentsListing(self, customer, interval, initialDate, finalDate):

        selectDate = ''
        if interval == 'day':
            selectDate = "p.paymentDate"
        else:
            selectDate = """CONCAT(CAST(year(p.paymentDate) AS CHAR) ,"-", CAST("""+interval+"""(p.paymentDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha, SUM(p.paymentAmount), tm.transactionType
                    FROM customers c, payments p, transactionType tT
                    WHERE tm.customers_customerId = c.customerId and
                        p.transactionType_idtransactionType = tm.transactionTypeId and
                        c.customerId = %s and
	                    p.paymentDate between %s and %s
                    GROUP BY """+ interval +"""(p.paymentDate)
					ORDER BY p.paymentDate
                """
        values = (customer.getIdCliente(), initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listPagos = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listPagos

    def customerTransactionsListing(self, customer, interval, initialDate, finalDate):

        selectDate = ''
        if interval == 'day':
            selectDate = "t.transactionDate"
        else:
            selectDate = """CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha,
                    SUM(dm.precio_unitario * dm.cantidad) as monto, tm.transactionType
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tm.customers_customerId and
                        m.transactionType_idtransactionType = tm.transactionTypeId and
                        m.transactionId = dm.transactions_transactionId and t.transactionStatus = 0 and
                        c.customerId = %s and
	                    t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (customer.getIdCliente(), initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        transactionsList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return transactionsList

    def selectEntradasTransacciones(self, interval, initialDate, finalDate):
        selectDate = ''
        if interval == 'day':
            selectDate = "t.transactionDate"
        else:
            selectDate = """CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha,
                    SUM(tD.unitPrice * tD.quantity) as amount, tm.transactionType
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tm.customers_customerId and
                        t.transactionType_idtransactionType = tm.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId and t.transactionStatus = 1 and
	                    t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listEntradaTransacciones = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listEntradaTransacciones


    def selectSalidaTransacciones(self, interval, initialDate, finalDate):
        selectDate = ''
        if interval == 'day':
            selectDate = "t.transactionDate"
        else:
            selectDate = """CONCAT(CAST(year(t.transactionDate) AS CHAR) ,"-", CAST("""+interval+"""(t.transactionDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha,
                    SUM(tD.unitPrice * tD.quantity) as monto, tm.transactionType
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tT.customers_customerId and
                        t.transactionType_idtransactionType = tm.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId and t.transactionStatus = 1 and
	                    t.transactionDate between %s and %s
                    GROUP BY """+ interval +"""(t.transactionDate)
					ORDER BY t.transactionDate
                """
        values = (initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listSalidaTransacciones = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listSalidaTransacciones


    def selectEntradaPagos(self, interval, initialDate, finalDate):
        selectDate = ''
        if interval == 'day':
            selectDate = "py.paymentDate"
        else:
            selectDate = """CONCAT(CAST(year(py.paymentDate) AS CHAR) ,"-", CAST("""+interval+"""(py.paymentDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha , SUM(py.paymentAmount), tm.transactionType
                    FROM customers c, payments py, transactionType tT
                    WHERE tm.customers_customerId = c.customerId and
                        py.transactionType_idtransactionType = tm.transactionTypeId and
	                    py.paymentDate between %s and %s
                    GROUP BY """+ interval +"""(py.paymentDate)
					ORDER BY p.paymentDate
                """
        values = (initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listEntradaPagos = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listEntradaPagos

    def selectSalidaPagos(self, interval, initialDate, finalDate):
        selectDate = ''
        if interval == 'day':
            selectDate = "p.paymentDate"
        else:
            selectDate = """CONCAT(CAST(year(p.paymentDate) AS CHAR) ,"-", CAST("""+interval+"""(p.paymentDate) AS CHAR))"""

        query = """
                    SELECT """+ selectDate +""" AS fecha , SUM(p.paymentAmount), tT.transactionType
                    FROM suppliers s, payments p, transactionType tT
                    WHERE tT.customers_customerId = s.supplierId and
                        p.transactionType_idtransactionType = tT.transactionTypeId and
	                    p.paymentDate between %s and %s
                    GROUP BY """+ interval +"""(p.paymentDate)
					ORDER BY p.paymentDate
                """
        values = (initialDate, finalDate)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listSalidaPagos = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return listSalidaPagos