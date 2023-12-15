#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Brand(object):

    def __init__(self):
        super(Brand, self).__init__()
        self.__brandId = 0
        self.__brandName = ""

    def setBrandId(self, brandId):
        self.__brandId = brandId

    def getBrandId(self):
        return self.__brandId

    def setBrandName(self, brand):
        self.__brandName = brand

    def getBrandName(self):
        return self.__brandName

	
