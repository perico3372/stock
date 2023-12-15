#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from connection.databaseConnection import DatabaseConnection
from model.supplier import Supplier
from model.product import Product
from model.category import Category
from model.brand import Brand

from PyQt5.QtWidgets import QComboBox

class ProductConnection(object):

    def __init__(self):
        self.databaseConnection = DatabaseConnection()
        self.product = Product()
        self.supplier = Supplier()
        self.category = Category()
        self.brand = Brand()

    def productListing(self, typeParameter, parameter, parameterState, parameterStock):
        query = """
                    SELECT pr.productId, pr.productName, pr.ProductDescription, CAST(TRUNCATE(pr.purchasePrice, 2) AS CHAR), CAST(TRUNCATE(pr.salesPrice, 2) AS CHAR),
                            pr.ProductGenre, pr.productStatus, pr.quantity, pr.minimumQuantity, b.brandId, b.brandName, c.categoryId,
                            c.categoryName, s.supplierId, ps.personName
                    FROM products pr, brands b , categories c, suppliers s, persons ps
                    WHERE pr.categories_categoryId = c.categoryId and ps.personId = s.persons_personId and pr.brands_brandId = b.brandId and
                        pr.suppliers_supplierId = s.supplierId and """+ typeParameter + """ LIKE %s and
                        pr.productStatus LIKE %s
                """
        param = parameter + '%'

        paramState = '1'
        if parameterState == 0:
            paramState = '%'

        if parameterStock == 1:
            query = query + " and pr.quantity > 0"

        values = (param, paramState)
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        listProducto = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        return listProducto

    # def updateProduct(self, product):
    #     query = """
    #                 UPDATE products
    #                 SET productName= %s, quantity= %s, productDescription= %s, categories_categoryId= %s, supplier_supplierId=%s,
    #                     brands_brandId= %s, purchasePrice= %s, salesPrice= %s, productStatus= %s, minimumQuantity= %s, ProductGenre= %s
    #                 WHERE productId= %s
    #             """
                
    #     categoryId = self.getCategoryId(product.getProductCategory())
    #     brandId = self.getBrandId(product.getProductBrand())
    #     supplierId = self.getSupplierId(product.getProductSupplier())        
        
    #     values = (product.getProductName(), product.getProductQuantity(), product.getProductDescription(), categoryId, supplierId,
    #               brandId(), product.getPurchasePrice(), product.getProductSalesPrice(), product.getProductStatus(),
    #               product.getProductMinimumQuantity(), product.getProductGenre(), product.getProductId()
    #              )
    #     self.databaseConnection.openConnection()
    #     self.databaseConnection.cursor.execute(query, values)
    #     self.databaseConnection.db.commit()
    #     self.databaseConnection.closeConnection()

    # def addProduct(self, product):
    #     query = """
    #                 INSERT INTO products (productName, quantity, ProductDescription, categories_categoryId,
    #                     supplier_supplierId, brands_brandId, purchasePrice, salesPrice, productStatus,
    #                     minimumQuantity, ProductGenre)
    #                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #             """
    #     try:
    #         categoryId = self.getCategoryId(product.getProductCategory())
    #         brandId = self.getBrandId(product.getProductBrand())
    #         supplierId = self.getSupplierId(product.getProductSupplier()) 
    #         values = (product.getProductName(), product.getProductQuantity(), product.getProductDescription(), categoryId, supplierId,
    #                   brandId, product.getPurchasePrice(), product.getProductSalesPrice(), product.getProductStatus(),
    #                   product.getProductMinimumQuantity(), product.getProductGenre()
    #                 )
            
    #         self.databaseConnection.openConnection()
    #         self.databaseConnection.cursor.execute(query, values)
    #         self.databaseConnection.db.commit()
    #         print(self.databaseConnection.cursor._check_executed())
    #         print(self.databaseConnection.cursor.messages)
    
    #     except Exception as e:
    #         # Handle the exception (log, print, etc.)
    #         print(f"Error adding product: {e}")
    
    #     finally:
    #         self.databaseConnection.closeConnection()

#     def addProduct(self, product):
#         # query = """
#         #     INSERT INTO products (productName, quantity, ProductDescription, categories_categoryId,
#         #         supplier_supplierId, brands_brandId, purchasePrice, salesPrice, productStatus,
#         #         minimumQuantity, ProductGenre)
#         #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         # """
#         query = """
#             INSERT INTO products (productName, quantity, ProductDescription, purchasePrice, salesPrice, productStatus,
#                 minimumQuantity, ProductGenre)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         try:
#             # categoryId = self.getCategoryId(product.getProductCategory())
#             # brandId = self.getBrandId(product.getProductBrand())
#             # supplierId = self.getSupplierId(product.getProductSupplier()) 
#             # values = (product.getProductName(), product.getProductQuantity(), product.getProductDescription(), categoryId, supplierId,
#             #           brandId, product.getPurchasePrice(), product.getProductSalesPrice(), product.getProductStatus(),
#             #           product.getProductMinimumQuantity(), product.getProductGenre()
#             #         )

#             values = (product.getProductName(), product.getProductQuantity(), product.getProductDescription(), 
#                        product.getPurchasePrice(), product.getProductSalesPrice(), product.getProductStatus(),
#                        product.getProductMinimumQuantity(), product.getProductGenre()
#                      )
            
#             #print("Values:", values)  # Imprime los valores antes de ejecutar la consulta
    
#             self.databaseConnection.openConnection()
#             self.databaseConnection.cursor.execute(query, values)
#             self.databaseConnection.db.commit()
    
#         except Exception as e:
#             # Handle the exception (log, print, etc.)
#             print(f"Error adding product: {e}")
# #            print("Values:", values)  # Imprime los valores en caso de error
    
#         finally:
#             self.databaseConnection.closeConnection()

        
    def addProduct(self, product):
        query = """
            INSERT INTO products (productName, quantity, ProductDescription, categories_categoryId,
                suppliers_supplierId, brands_brandId, purchasePrice, salesPrice, productStatus,
                minimumQuantity, ProductGenre)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            values = (product.getProductName(), product.getProductQuantity(), product.getProductDescription(), 
                      product.getProductCategory().getCategoryId(), product.getProductSupplier().getSupplierId(),
                    product.getProductBrand().getBrandId(), product.getPurchasePrice(), product.getProductSalesPrice(), 
                    product.getProductStatus(), product.getProductMinimumQuantity(), product.getProductGenre()
                    )
            print("Values:", values)  # Imprime los valores antes de ejecutar la consulta

            self.databaseConnection.openConnection()
            self.databaseConnection.cursor.execute(query, values)
            self.databaseConnection.db.commit()
    
        except Exception as e:
            # Handle the exception (log, print, etc.)
            print(f"Error adding product: {e}")
            print("Values:", values)  # Imprime los valores en caso de error
    
        finally:
            self.databaseConnection.closeConnection()
    



    def deleteProduct(self, product):
        query = """
                    UPDATE products
                    SET productStatus = 0
                    WHERE productId = %s
                """
        values = product.getProductId()
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query, values)
        self.databaseConnection.closeConnection()

    def brandsListing(self):
        
        query = "SELECT brandId,brandName FROM brands"
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        auxBrandList = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        brandList = [(0, '')]
        
        for brand in auxBrandList:
            brandList.append((brand[0], brand[1]))
            
        return brandList
    
    def categoriesListing(self):
    
        query = "SELECT categoryId, categoryName FROM categories"
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        auxListCategories = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        
        categoriesList = [(0,'')]  # Inicializa la lista con una tupla vacía al principio
        
        for category in auxListCategories:
            categoriesList.append((category[0], category[1]))
        
        return categoriesList

    def suppliersListing(self):
        query = "SELECT ps.personName, s.supplierId FROM persons ps, suppliers s WHERE ps.personId = s.persons_personId"
        
        self.databaseConnection.openConnection()
        self.databaseConnection.cursor.execute(query)
        auxListSupplier = self.databaseConnection.cursor.fetchall()
        self.databaseConnection.closeConnection()
        
        # Crear una lista de tuplas (ID, nombre) para los proveedores
        suppliersList = [(str(supplier[1]), supplier[0]) for supplier in auxListSupplier]
        
        # Agregar un elemento vacío al principio de la lista
        suppliersList.insert(0, (0, ''))
        
        return suppliersList


   
# Si estás ejecutando este script como un programa independiente
if __name__ == "__main__":
    # Crear una instancia de la clase ConexionProducto
    products = ProductConnection()

    # Llamar al método listProveedor para obtener la lista de proveedores
    lista_marcas = products.brandsListing()
    lista_categorias = products.categoriesListing()
    lista_proveedores = products.suppliersListing()
    agregar = products.addProduct()
    
    print(lista_marcas)    
    print(lista_categorias)
    print(lista_proveedores)

    