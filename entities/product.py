
from data import create_default_repo
from .user import User, UserObject
from data.database import SubstringType

class ProductCategory:
     FASHION = "fashion"
     GROCERIES = "groceries"
     ELECTRONICS = "electronics"
     SPORTS = "sports"
     BOOKS = "books"
     STATIONARY = "stationary"
     FURNITURE = "furniture"
     HEALTH = "health"
     


class Product:
     def __init__(self,id:int, name: str, category:ProductCategory,price: float, brand:str, description:str, stock:int, vendor):
          # instance variables initailzation
          self.id = id
          self.name = name
          self.category = category
          self.price = price
          self.brand = brand
          self.description = description
          self.stock = stock
          self.vendor = vendor
          
     def new_instance(name: str, category:ProductCategory,price: float, brand:str, description:str, stock:int, vendor):
          return Product(0,name,category,price,brand,description,stock, vendor)
     

     def save(self):
          repo = create_default_repo()
          
          new_id = repo.new_entry("product",
               ["category","price","brand","description","stock", "name", "vendor"],
               [f"'{self.category}'",self.price,f"'{self.brand}'",f"'{self.description}'",self.stock,f"'{self.name}'", self.vendor]
          )
          
          self.id = new_id
          
          repo.close()
          
     def query_instance(column, value):
          repo = create_default_repo()
          
          data = repo.query_one("product", column, value)
          repo.close()
          
          return Product._to_product(data)
     
     def query_all()->list:
          repo = create_default_repo()
          
          data =  repo.query_all("product")
          repo.close()
          
          prod_list = []
          
          for i in data:
               pr = Product._to_product(i)
               prod_list.append(pr)
          
          return prod_list
          
               
     def delete(self):
          repo = create_default_repo()
          repo.delete("product", "product_id", str(self.id))
          repo.close()
          
     def query_all_instance(column, value)->list:
          repo = create_default_repo()   
          data =  repo.query("product",column, value)
          repo.close()
          product_list = []
          for product in data:
               pr = Product._to_product(product)
               product_list.append(pr)
          
          return product_list
     
     '''------------------FETCH-QUERY-------------------'''
     def query_by_id(id):
          return Product.query_instance("product_id", id)
     
     def query_by_name(name):
          return Product.query_all_instance("name", name)
     
     def query_by_category(category):
          return Product.query_all_instance("category", category)
     
     def query_by_price(price):
          return Product.query_all_instance("price", price)
     
     def query_by_brand(brand):
          return Product.query_all_instance("brand", brand)
     
     def query_by_description(description):
          return Product.query_all_instance("description", description)
     
     def query_by_stock(stock):
          return Product.query_all_instance("stock", stock)
     
     def query_by_vendor(vendor):
          return Product.query_all_instance("vendor", vendor)
     
     
     '''A method that querries all products based on substring values provided'''
     def query_by_name_substring(substring):
          repo = create_default_repo()
          
          data = repo.query_substring(
               table="product", 
               column="name", 
               substring=substring, 
               type=SubstringType.BETWEEN
          )
          repo.close()
          
          product_list = []
          
          for product in data:
               pr = Product._to_product(product)
               product_list.append(pr)
          return product_list
          
     
     '''------------------UPDATE-QUERY-------------------'''
     def update(self, field, value):
          repo = create_default_repo()
          repo.alter_entry("product", [field], [value], "product_id", str(self.id))
          repo.close()


     def update_name(self, name):
          self.name = name          
          self.update( "name", self.name)
     def update_category(self, category):
          self.category = category          
          self.update( "category", self.category)
     def update_price(self, price):
          self.price = price          
          self.update( "price", self.price)
     def update_brand(self, brand):
          self.brand = brand          
          self.update( "brand", self.brand)
     def update_description(self, description):
          self.description = description
          self.update( "description", self.description)
     def update_stock(self, stock):
          self.stock = stock  
          self.update( "stock", self.stock)
          
          
     # __init__(self,id:int, name: str, category:ProductCategory,price: float, brand:str, description:str, stock:int, vendor):
     def _to_product(data):
          if data != None:
               return Product(data[0], data[6], data[1], data[2], data[3], data[4], data[5], data[7])
          return None
     
     
class ProductObject:
     def __init__(self, id:int,  category:ProductCategory,price: float, brand:str, description:str, stock:int,name: str, vendor):
          # instance variables initailzation
          self.id = id
          self.name = name
          self.category = category
          self.price = price
          self.brand = brand
          self.description = description
          self.stock = stock
          self.vendor = vendor
          
     def parse(data):
          if data == None:
               return data
          return ProductObject(data[0],data[1],data[2],data[3],data[4],data[5],data[6], data[7])
     def product_to_object(data:Product):
          if data == None:
               return data
          
          
          # parsing vendor id to vendor object
          vendor = User.query_by_id(data.vendor)
          vendor_object = UserObject.user_to_object(vendor)
          
          return ProductObject(
               id = data.id,
               category=data.category,
               price=data.price,
               brand=data.brand,
               description=data.description,
               stock=data.stock,
               name=data.name,
               vendor=vendor_object
          )
          
     def products_to_objects(data:list):
          if data == None:
               return data
          return [ProductObject.product_to_object(i) for i in data]
