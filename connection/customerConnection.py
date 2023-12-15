#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.customer import Customer

class CustomerConnection(object):

    def __init__(self):
       self.databaseConnection = DatabaseConnection()
       self.customer = Customer()

    def customersListing(self, typeParameter, parameter, parameterState):
        query = """
                    SELECT c.customerId, ps.personName, ps.personEmail, 
                           a.streetAddress, a.numberAddress, a.floorAddress, a.dptoAddress, a.addressId, 
                           ps.personId, c.customerStatus
                    FROM customers c, persons ps, addresses a
                    WHERE ps.personId = c.persons_personId and a.addressId = ps.addresses_addressId and
                    """ +typeParameter + """ LIKE %s and c.customerStatus LIKE %s
                """
        paramState = '1'
        if parameterState == 0:
            paramState = '%'

        param = parameter+ '%'
        values = (param, paramState)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        customerList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return customerList

    def listCustomersPhones(self, customer):
        query = """SELECT ph.phoneId, ph.numberPhone, ph.typePhone
                    FROM phones ph, persons ps, customers c
                    WHERE ps.personsId = c.persons_personId and ps.personsId = ph.persons_personId
                    and c.customerId = %s"""
        values = customer.getCustomerId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        phoneList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return phoneList

    def updateCustomers(self, customer):

        query = """UPDATE persons ps, customers c, adresses a
                    SET ps.personName = %s , ps.personEmail= %s , a.streetAddress= %s, a.numberAddress = %s, a.floorAddress = %s, d.dptoAddress = %s, c.customerStatus = %s
                    WHERE ps.personId = c.persons_personId and ps.addresses_addressId = a.idadresses
                            and c.idcustomers = %s"""
        values = (customer.getPersonName(), customer.getPersonEmail(), customer.getPersonAddress().getAddressStreet(),
                  customer.getPersonAddress().getAddresNumber(), customer.getPersonAddress().getAddressFloor(),
                  customer.getPersonAddress().getAddressDpto(), customer.getCustomerStatus(), customer.getCustomerId())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def addCustomers(self, customer):
        self.databaseConnection.openConnection()

        addressesQuery = "INSERT INTO addresses (streetAddress, numberAddress, floorAddress, dptoAddress) VALUES (%s, %s, %s, %s)"

        addressesValues = (customer.getAddressStreet(), customer.getAddressNumber(),
                            customer.getAddressFloor(), customer.getAddressDpto())
        self.databaseConnection.cursor.execute(addressesQuery, addressesValues)

        personsQuery = "INSERT INTO persons (personName, personEmail, addresses_addressId) VALUES (%s, %s, LAST_INSERT_ID())"
        personsValues = (customer.getPersonName(), customer.getPersonEmail())
        self.databaseConnection.cursor.execute(personsQuery, personsValues)

        customerInquiry = "INSERT INTO customers (persons_personId, CustomerStatus) VALUES (LAST_INSERT_ID(), %s)"
        customerValues = (customer.getPersonStatus())
        self.databaseConnection.cursor.execute(customerInquiry, customerValues)

        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def deleteCustomers(self, customer):
        customerInquiry = """
                            UPDATE customers
                            SET customerStatus = 0
                            WHERE customersId = %s
                       """
        customerValues = customer.getIdCliente()

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(customerInquiry, customerValues)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()