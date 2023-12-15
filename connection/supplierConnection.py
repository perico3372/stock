#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.supplier import Supplier
from connection.databaseConnection import DatabaseConnection

class SupplierConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.supplier = Supplier()

    def suppliersListing(self, typeParameter, parameter, parameterState):

        
        
        query ="""
                    SELECT s.supplierId, s.supplierDescription, ps.personName, ps.personEmail, s.supplierWeb, 
                    a.streetAddress, a.numberAddress, a.floorAddress, a.dptoAddress, ps.personId, 
                    a.addressId, s.supplierStatus
                    FROM suppliers s, persons ps, addresses a
                    WHERE ps.addresses_addressId = a.addressId and ps.personId = s.persons_personId and
                    """ + typeParameter + """ LIKE %s and s.supplierStatus LIKE %s
                """
        param = parameter + '%'

        paramState = '1'
        if parameterState == 0:
            paramState = '%'

        values = (param, paramState)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listProveedor = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return listProveedor

    def suppliersPhonesListing(self, supplier):
        query = """SELECT ph.phoneId, t.numberPhone, t.typePhone
                    FROM phone ph, persons ps, suppliers s
                    WHERE ps.personsId = s.persons_personId and ps.personsId = ph.persons_personId
                    and s.supplierId = %s"""
        value = supplier.getSupplierId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        phoneList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return phoneList

    def updateSuppliers(self, supplier):
        query = """
                    UPDATE persons ps, suppliers s, addresses a
                    SET ps.personName = %s , ps.emailPerson= %s , s.supplierDescription = %s, s.supplierWeb = %s, a.streetAddress= %s,
                            a.numberAddress = %s, a.floorAddress = %s, a.dptoAddress = %s, s.supplierStatus = %s, s.supplierId = %s
                    WHERE ps.personsId = s.persons_personsId and ps.addresses_addressId = a.addressId
                            and s.supplierId = %s
                """
        values = (supplier.getPersonName(), supplier.getPersonEmail(), supplier.getSupplierDescription(),
                    supplier.getSupplierWeb(), supplier.getAddressStreet(), supplier.getAddresNumber(),
                    supplier.getAddressFloor(), supplier.getAddressDpto(), supplier.getPersonStatus(),
                    supplier.getSupplierId()
        )
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()
    

    def addSuppliers(self, supplier):
        try:
            self.databaseConnection.openConnection()
    
            # Insertar dirección
            addressQuery = "INSERT INTO addresses (streetAddress, numberAddress, floorAddress, dptoAddress) VALUES (%s, %s, %s, %s)"
            addressValues = (supplier.getAddressStreet(), supplier.getAddressNumber(),
                             supplier.getAddressFloor(), supplier.getAddressDpto())
            self.databaseConnection.cursor.execute(addressQuery, addressValues)
            

    
            # Insertar persona
            personQuery = "INSERT INTO persons (addresses_addressId, personName, personEmail) VALUES (%s, %s, %s)"
            personValues = (self.databaseConnection.cursor.lastrowid, supplier.getPersonName(), supplier.getPersonEmail())
            self.databaseConnection.cursor.execute(personQuery, personValues)
    
            # Insertar proveedor
            query1 = "INSERT INTO suppliers (persons_personId, supplierWeb, supplierStatus) VALUES (LAST_INSERT_ID(), %s, %s)"
            values1 = (supplier.getSupplierWeb(), supplier.getPersonStatus())
            self.databaseConnection.cursor.execute(query1, values1)
    
            self.databaseConnection.db.commit()
            print("OK")
            return True  # Return True if everything is successful
    
        except Exception as e:
            print("Error:", e)
            return False  # Return False if an exception occurs
        finally:
            self.databaseConnection.closeConnection()
    



    def deleteSuppliers(self, supplier):
        supplierQuery = """
                            UPDATE suppliers
                            SET supplierStatus = 0
                            WHERE suppliers.supplierId = %s
                           """
        supplierValues = supplier.getSupplierId()

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(supplierQuery, supplierValues)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()