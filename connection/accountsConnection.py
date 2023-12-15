
import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection

class AccountsConnection():

    def __init__(self):
        self.databaseConnection = DatabaseConnection()

    def customersTransactionsListing(self):
        query = """
                    SELECT c.customerId, p.namePerson, SUM(tD.unitPrice * tD.quantity ) as amount
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD, persons p
                    WHERE c.idclientes = tT.customers_customerId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId and
                        t.status = 0 and
                        p.personsId = c.persons_personId
                    GROUP BY tT.customers_customerId
                    ORDER BY amount desc
                """
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        customerList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return customerList

    def customersPaymentsListing(self):
        query = """
                    SELECT c.customerId, SUM(py.paymentAmount)
                    FROM customer c, payments py, transactionType tT
                    WHERE tT.customers_customerId = c.customerId and
                        py.transactionType_transactionTypeId = tT.transactionTypeId
                    GROUP BY c.customerId
                """
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        customerList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return customerList

    def suppliersTransactionsListing(self):
        query = """
                    SELECT s.supplierId, p.namePerson, SUM(tD.unitPrice * tD.quantity ) as amount
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD, persons p
                    WHERE s.supplierId = tT.suppliers_supplierId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId and
                        t.status = 0 and
                        p.personsId = s.persons_personId
                    GROUP BY tT.suppliers_supplierId
                    ORDER BY amount desc
                """
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        suppliersList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return suppliersList

    def suppliersPaymentsListing(self):
        query = """
                    SELECT s.supplierId, SUM(py.paymentAmount)
                    FROM  suppliers s, payments py, transactionType tT
                    WHERE tT.suppliers_supplierId = s.supplierId and
                        py.transactionType_transactionTypeId = tT.transactionTypeId
                    GROUP BY s.supplierId
                """

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        suppliersList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return suppliersList

