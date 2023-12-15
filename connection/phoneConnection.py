#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from model.phone import Phone
from connection.databaseConnection import DatabaseConnection

class PhoneConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.phone = Phone()

    def phoneListing(self, phone):
        query ="""
                    SELECT ph.phoneId, ph.typePhone, t.numberPhone
                    FROM phone ph, persons ps
                    WHERE ph.persons_personsId = ps.personsId and ps.personsId = %s
                """
        values = phone.getPersonId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        phoneList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return phoneList

    def updatePhone(self, phone):
        query = """
                    UPDATE phones
                    SET phoneNumber = %s , phoneType = %s
                    WHERE phoneId= %s;
                """
        values = (phone.getPhoneNumber(), phone.getPhoneType(), phone.getPhoneId())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def addPhone(self, phone):
        query = "INSERT INTO phones (phoneNumber, phoneType, persons_personId) VALUES (%s , %s, %s)"
        values = (phone.getPhoneNumber(), phone.getPhoneType(), phone.getPhoneId())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()


    def addPhoneInit(self, phones):
        self.databaseConnection.openConnection()

        personaIdQuery = "select MAX(personId) from persons"
        self.databaseConnection.cursor.execute(personaIdQuery)
        result = self.databaseConnection.cursor.fetchall()

        personId = int(result[0][0])

        for phone in phones:
            if phone[2] != '':
                query = "INSERT INTO phones (phoneNumber, phoneType, persons_personId) VALUES (%s , %s, %s)"
                values = (phone[2], phone[1], personId)
                self.databaseConnection.cursor.execute(query, values)
                self.databaseConnection.db.commit()

        self.databaseConnection.closeConnection()


    def deletePhone(self, phone):
        query = """
                    DELETE FROM phones
                    WHERE phoneId= %s
                """
        values =phone.getPhoneId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

