
from data import create_default_repo
from .user import User, UserObject
from .product import Product, ProductObject



class Cart:
     def __init__(self, cart_id, user_id, product_id, quantity):
          self.cart_id = cart_id
          self.user_id = user_id
          self.product_id = product_id
          self.quantity = quantity
          
     def new_instance(user_id, product_id, quantity):
          return Cart(0, user_id, product_id, quantity)
     
     def save(self):
          repo = create_default_repo()
          
          new_id = repo.new_entry("cart", ["user", "product", "quantity"], [self.user_id, self.product_id, self.quantity])
          self.cart_id = new_id
          
          
          repo.close()
          
     def delete(self):
          repo = create_default_repo()
          repo.delete("cart", "cart_id", str(self.cart_id))
          repo.close()

     def query_instance(column, value):
          repo = create_default_repo()
          
          data = repo.query_one("cart", column, value)
          repo.close()
          
          return Cart._to_cart(data)
     
     def query_all_instaces(column, value):
          repo = create_default_repo()
          
          data = repo.query("cart", column, value)
          repo.close()
          
          cart_list = []
          
          for cart in data:
               cart_list.append(Cart._to_cart(cart))
          
          return cart_list
     
     def query_all():
          repo = create_default_repo()
          
          data =  repo.query_all("cart")
          repo.close()
          
          cart_list = []
          
          for cart in data:
               cart_list.append(Cart._to_cart(cart))
          
          return cart_list
     
     def query_on_multiple_conditions(columns:list, values:list):
          repo = create_default_repo()
          
          data = repo.query_on_multiple_conditions("cart", columns, values)
          repo.close()
          
          cart_list = []
          
          for cart in data:
               cart_list.append(Cart._to_cart(cart))
          
          if len(cart_list) == 0:
               return None
          
          return cart_list
     
     '''------------------FETCH-QUERY-------------------'''
     def query_by_cart_id(cart_id):
          return Cart.query_instance("cart_id", cart_id)
     
     def query_by_user_id(user_id):
          return Cart.query_all_instaces("user", user_id)
     
     def query_by_product_id(product_id):
          return Cart.query_all_instaces("product", product_id)
     
     def query_by_quantity(quantity):
         return Cart.query_all_instaces("quantity", quantity)
               
     '''------------------UPDATE-QUERY-------------------'''
     
     def update(self, field, value):
          repo = create_default_repo()
          
          repo.alter_entry("cart", [field], [value], "cart_id", str(self.cart_id))
          
          repo.close()
     
     def update_quantity(self, quantity):
          self.quantity = quantity          
          self.update("quantity", self.quantity)
          


     def update_user_id(self, user_id):
          self.user_id = user_id          
          self.update("user_id", self.user_id)
          
     def update_product_id(self, product_id):
          self.product_id = product_id  
          self.update("product_id", self.product_id)
          
     def _to_cart(data):
          if data==None:
               return None
          
          return Cart(data[0],data[1],data[2],data[3])
     
class CartObject:
     def __init__(self, cart_id, user_obj, product_obj, quantity):
          self.cart_id = cart_id
          self.user = user_obj
          self.product = product_obj
          self.quantity = quantity
          
     def parse(data):
          if data == None:
               return data
          
          user_id = data[1]
          user_obj = User.query_by_id(user_id)
          
          prod_id = data[2]
          prod_obj = Product.query_by_id(prod_id)
          
          return CartObject(data[0],user_obj,prod_obj,data[3])
     
     
     def cart_to_object(data:Cart):
          if data == None:
               return data
          
          user = User.query_by_id(data.user_id)
          user_obj = UserObject.user_to_object(user)
          
          product = Product.query_by_id(data.product_id)
          product_obj = ProductObject.product_to_object(product)
          
          return CartObject(data.cart_id,user_obj,product_obj,data.quantity)
     
     def carts_to_objects(data:list):
          if data == None:
               return data
          
          return [CartObject.cart_to_object(i) for i in data]
