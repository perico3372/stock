
import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.customer import Customer
from model.supplier import Supplier
import datetime

class PaymentConnection(object):

    def __init__(self):
        self.databseConnection = DatabaseConnection()
        self.customer = Customer()
        self.supplier = Supplier()

    def listSuppliers(self, parameterType, parameter):
        query = """
                    SELECT s.supplierId , s.supplierDescription, ps.namePerson, ps.emailPerson
                    FROM suppliers s, persons ps
                    WHERE ps.personId = s.persons_personId and s.suplierStatus = 1 and
                    """ + parameterType + """ LIKE %s
                """
        parameter = parameter + '%'
        values = parameter
        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        suppliersList = self.databseConnection.cursor.fetchall()

        self.databseConnection.closeConnection()

        return suppliersList


    def customersListing(self, parameterType, parameter):
        query = """
                    SELECT c.customerId, ps.namePerson, p.emailPerson
                    FROM customers c, persons ps
                    WHERE ps.personId = c.persons_personId and c.status = 1 and
                    """+ parameterType + """ LIKE %s
                """
        parameter = parameter + '%'
        values = parameter
        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        listCustomers = self.databseConnection.cursor.fetchall()
        self.databseConnection.closeConnection()

        return listCustomers


    def suppliersPaymentsListing(self, supplier):
        query = """
                    SELECT py.datePayment, py.paymentAmount, tm.transactionType
                    FROM suppliers s, payments py, transactionType tT
                    WHERE tm.suppliers_supplierId = s.supplierId and
                        py.transactionType_idtransactionType = tm.transactionTypeId and
                        s.supplierId = %s
                """
        values = supplier.getSupplierId()
        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        paymentsList = self.databseConnection.cursor.fetchall()
        self.databseConnection.closeConnection()

        return paymentsList

    def suppliersTransactionsListing(self, supplier):
        query = """
                    SELECT t.transactionDate, SUM(tD.unitPrice * tD.quantity) as amount, tT.transactionType
                    FROM suppliers s, transactions t, transactionType tT, transactionDetail tD
                    WHERE s.supplierId = tT.suppliers_supplierId and
                        t.transactionType_idtransactionType = tm.transactionTypeId and
                        t.transactionId = tD.transactions_transactionId and t.status = 0 and
                        s.supplierId = %s
                    GROUP BY m.transactionDate
                """
        values = supplier.getSupplierId()

        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        listTransactions = self.databseConnection.cursor.fetchall()
        self.databseConnection.closeConnection()

        return listTransactions

    def customersPaymentsListing(self, customer):
        query = """
                    SELECT py.datePayment, py.paymentAmount, tm.transactionType
                    FROM customers c, payments py, transactionType tT
                    WHERE tT.customers_customerId = c.customerId and
                        py.transactionType_idtransactionType = tT.transactionTypeId and
                        c.customerId = %s
                """
        values = customer.getCustomerId()
        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        paymentsList = self.databseConnection.cursor.fetchall()
        self.databseConnection.closeConnection()

        return paymentsList

    def customersTransactionsListing(self, customer):
        query = """
                    SELECT t.transactionDate, SUM(tD.unitPrice * tD.quantity) as amount, tT.transactionType
                    FROM customers c, transactions t, transactionType tT, transactionDetail tD
                    WHERE c.customerId = tT.customers_customerId and
                        t.transactionType_idtransactionType = tT.transactionTypeId and
                        t.idmovimiento = tD.transactions_transactionId and t.status = 0 and
                        c.customerId = %s
                    GROUP BY t.transactionDate
                """
        values = customer.getCustomerId()

        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(query, values)
        listTransactions = self.databseConnection.cursor.fetchall()
        self.databseConnection.closeConnection()

        return listTransactions

    def loadPaymentsCustomers(self, customer, amount):
        today = datetime.datetime.now().date()

        self.databseConnection.openConnection()

        transactionTypeQuery = """
                                INSERT INTO transactionType (transactionType, customers_customerId)
                                VALUES ('pago', %s)
                              """
        transactionTypeValues = customer.getCustomerId()

        self.databseConnection.cursor.execute(transactionTypeQuery, transactionTypeValues)
        self.databseConnection.db.commit()
        transactionTypeId = self.databseConnection.cursor.lastrowid
        cantRowAffect = self.databseConnection.cursor.rowcount
        self.databseConnection.closeConnection()

        paymentsQuery = """
                            INSERT INTO payments (paymentDate, paymentAmount, transactionType_idtransactionType)
                            VALUES (%s, %s, %s);

                          """
        paymentsValues = (today, amount, transactionTypeId)
        self.databseConnection.openConnection()
        self.databseConnection.cursor.execute(paymentsQuery, paymentsValues)
        self.databseConnection.db.commit()
        receiptId = self.databseConnection.cursor.lastrowid
        self.databseConnection.closeConnection()

        return receiptId

    def loadPaymentsSuppliers(self, supplier, amount):
        today = datetime.datetime.now().date()

        self.databseConnection.openConnection()

        transactionTypeQuery = """
                                INSERT INTO transactionType (transactionType, suppliers_supplierId)
                                VALUES ('pago', %s)
                              """
        transactionTypeValues = supplier.getSupplierId()

        self.databseConnection.cursor.execute(transactionTypeQuery, transactionTypeValues)
        self.databseConnection.db.commit()
        transactionTypeId = self.databseConnection.cursor.lastrowid
        cantRowAffect = self.databseConnection.cursor.rowcount


        paymentsQuery = """
                            INSERT INTO payments (paymentDate, paymentAmount, transactionType_idtransactionType)
                            VALUES (%s, %s, %s);

                          """
        paymentsValues = (today, amount, transactionTypeId)

        self.databseConnection.cursor.execute(paymentsQuery, paymentsValues)
        self.databseConnection.db.commit()
        receiptId = self.databseConnection.cursor.lastrowid
        self.databseConnection.closeConnection()

        return receiptId