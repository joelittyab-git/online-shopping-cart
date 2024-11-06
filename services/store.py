from entities.product import Product
from entities.product import ProductCategory, ProductObject
from entities.user import User, UserObject
from data import create_default_repo


class StoreService:
     def __init__(self, name, certificate):
          self.name = name
          self.certificate = certificate
          
     def fetch_products_by_category(self, category):
          products = Product.query_by_category(category)
          return ProductObject.products_to_objects(products)
     
     def fetch_categories(self):
          repo = create_default_repo()
          data = repo.query_distinct("product", "category")          
          repo.close()
          return [category[0] for category in data]

     def fetch_all_categories(self):
          repo = create_default_repo()
          data = repo.query_enum_types("product", "category")
          repo.close()
          return data

     def fetch_brands(self):
          repo = create_default_repo()
          data = repo.query_distinct("product", "brand")
          repo.close()
          return [brand[0] for brand in data]
          
     def fetch_by_name(self, name):
          return  ProductObject.products_to_objects(
               data = Product.query_by_name_substring(name)
          )
          
     def fetch_by_vendor(self, vendor_name):
          users=User.query_by_vendor_name_substring(vendor_name)
          if len(users) == 0:
               return None

          prod_list = []
          for user in users:
               user:User = user     
               vendor_id = user.user_id
               prod_objects = ProductObject.products_to_objects(
                    Product.query_by_vendor(vendor_id)
               )
               prod_list.extend(prod_objects)
          return prod_list
          
     def fetch_by_brand(self, brand_name):
          return ProductObject.products_to_objects(
               Product.query_by_brand(brand_name)
          )
          
     def fetch_all_products(self):
          return ProductObject.products_to_objects(
               Product.query_all()
          )
