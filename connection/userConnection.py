#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.user import User

class UserConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.user = User()

    def userListing(self, typeParameter, parameter):
        query = """
                    SELECT u.userId, ps.personName, u.userName, u.userType, u.userPassword, ps.personEmail, a.streetAddress,
                            a.numberAddress, a.floorAddress, a.dptoAddress, a.addressId, ps.personId
                    FROM users u , persons ps, addresses a
                    WHERE ps.personId = u.persons_personId and ps.addresses_addressId = a.addressId and
                    """ + typeParameter + """ LIKE %s
                """
        param = parameter + '%'
        values = param
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        userList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return userList

    def UserPhoneListing(self, user):
        query = """
                    SELECT ph.phoneId, ph.phoneNumber, ph.phoneType
                    FROM phones ph, persons p, users u,
                    WHERE p.personId = u.persons_personId and p.personId = ph.persons_personId
                    and u.userId = %s
                """
        values = user.getUserId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        phoneList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return phoneList

    def updateUsers(self, user):
        query = """
                    UPDATE persons p, users u, addresses a
                    SET p.personName = %s , p.emailPerson= %s, u.lastName = %s, u.userName = %s,
                        u.userType = %s, u.userPassword = %s, a.streetAddress = %s, a.numberAddress = %s, a.floorAddress = %s, a.dptoAddress = %s
                    WHERE p.personsId = u.persons_personsId and p.addresses_addressId = a.addressId
                        and u.userId = %s
                """
        values = (user.getName(), user.getEmailPerson(), user.getLastName(), user.getUser(),
                  user.getUserType(), user.getPasswd(), user.getAddress().getAddress(),
                  user.getAddress().getNumber(), user.getAddress().getFloor(),
                  user.getAddress().getDpto(), user.getUserId())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def addUsers(self, user):
        self.databaseConnection.openConnection()

        addressQuery = "INSERT INTO addresses (streetAddress, numberAddress, floorAddress, dptoAddress) VALUES (%s, %s, %s, %s)"
        addressValues = (user.getAddressStreet(), user.getAddressNumber(),
                            user.getAddressFloor(), user.getAddressDpto())
        self.databaseConnection.cursor.execute(addressQuery, addressValues)

        personQuery = "INSERT INTO persons (personName, personEmail, addresses_addressId) VALUES (%s, %s, LAST_INSERT_ID())"
        personValues = (user.getPersonName(), user.getPersonEmail())
        self.databaseConnection.cursor.execute(personQuery, personValues)

        userQuery = """INSERT INTO users (userType, persons_personId, userPassword, userName)
                        VALUES ( %s , LAST_INSERT_ID() , %s , %s )"""
        userValues = (user.getUserType(), user.getUserPasswd(), user.getUserName())
        self.databaseConnection.cursor.execute(userQuery, userValues)

        self.databaseConnection.db.commit()
        self.databaseConnection.closeConnection()

    def deleteUsers(self, user):
        phoneQuery = """
                            DELETE phones
                            FROM phones
                            WHERE phones.persons_personsId = %s
                        """
        phoneValues = user.getPersonId()

        userQuery = """
                            DELETE users
                            FROM users
                            WHERE users.userId = %s
                       """

        userValues = user.getUserId()

        personQuery = """
                            DELETE persons
                            FROM persons
                            WHERE persons.personsId = %s
                       """

        personValues = user.getPersonId()

        addressQuery = """
                            DELETE addresses
                            FROM addresses
                            WHERE addresses.addressId = %s
                         """

        addressValues = user.getAddress().getIdDireccion()

        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(phoneQuery, phoneValues)
        self.databaseConnection.db.commit()
        self.databaseConnection.cursor.execute(userQuery, userValues)
        self.databaseConnection.db.commit()
        self.databaseConnection.cursor.execute(personQuery, personValues)
        self.databaseConnection.db.commit()
        self.databaseConnection.cursor.execute(addressQuery, addressValues)
        self.databaseConnection.db.commit()

        self.databaseConnection.closeConnection()


    def connectionUserValidateUser(self, user):
        query = "SELECT userName, userType FROM users WHERE userName= %s and userPassword = %s"
        values = (user.getUserName(), user.getUserPasswd())
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        userAux = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()

        return userAux
