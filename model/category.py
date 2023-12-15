#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Category(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__categoryId = 0
        self.__category = ""

    def setCategoryId(self, categoryId):
        self.__categoryId = categoryId

    def getCategoryId(self):
        return self.__categoryId

    def setCategoryName(self, category):
        self.__category = category

    def getCategoryName(self):
        return self.__category



    
        