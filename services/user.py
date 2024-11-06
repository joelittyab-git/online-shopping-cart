
from entities.user import User, UserObject, UserType
from entities.cart import Cart, CartObject
from entities.product import ProductObject, Product
from entities.tx import Transaction, TransactionMethod
from entities.orders import Order, OrderStatus, OrderObject

class UserSession:
     def __init__(self, user_id, username, type, email, address, telephone, first_name, 
               last_name):
               self.user_id = user_id
               self.username = username
               self.type = type
               self.email = email
               self.address = address
               self.telephone = telephone
               self.first_name = first_name
               self.last_name = last_name
               
class UserService:
     def __init__(self, session = None):
          self.session = session
     
     '''User authentication'''
     def login(self, username, password):
          user = User.query_by_username(username)
          if user==None:
               return None
          elif user.password == password:
               storage = UserSession(user.user_id, user.username, user.type, user.email,
				user.address, user.telephone, user.first_name, user.last_name)
               self.session = storage
               return storage

          else:
               return None       
     
     def retrieve_user(self, username):
          user = User.query_by_username(username)
          if user==None:
               return None
          else:
               return user
     
     def authenticate(self, password):
          user = User.query_by_id(self.session.user_id)
          if self.session == None:
               return False
          elif user.password == password:
               return True
          else:
               return False
          
     def register_customer(self, username, email, address, telephone, first_name,
		last_name, password, account_type:UserType):
          user = User.query_by_username(username)
          if user!=None:
               return {
                    "status": False,
                    "invalid_fields": ["username"],
               }
               
          User.new_instance(username, email,account_type, address, telephone, 
			first_name, last_name, password).save()
          return {
               "status": True,
               "invalid_fields": [],
          }
          
          
     def reset_password(self, username, password):
          user = User.query_by_username(username)
          if user == None:
               return None
          else:
               user.update_password(password)
          
     def add_to_cart(self, product:ProductObject, quantity):
          self.authorize()
          
          product_id = product.id
          user_id = self.session.user_id
          
          # checks if an entry of the same product on the same user exists
          entries = Cart.query_on_multiple_conditions(["user", "product"], [user_id, 
				product_id])
          
          if entries == None:
               # if there is no exisitng product in the cart for the user new instance is 
      		# created
               # adding a new cart instance 
               cart = Cart.new_instance(
                    user_id=user_id,
                    product_id=product.id,
                    quantity=quantity
               )
               cart.save()
               
          elif len(entries)>1:
               # if there exists an existing cart entry/entries for the user, combines all of them by adding the quantity and deleteing all instances and creating new
               qty = 0
               
               # interating through the cart items and adding their quantuities to new entry and deleting them 
               for entry in entries:
                    entry:Cart = entry
                    qty += entry.quantity
                    entry.delete()
               qty = len(entries) + quantity
               
               Cart.new_instance(
                    user_id=user_id,
                    product_id=product.id,
                    quantity=qty
               ).save()
               
          else:
               # If only one entry of it exists   
               print("Entered last")
               entry:Cart = entries[0]
               entry.update_quantity(entry.quantity+quantity)

          
     def remove_from_cart(self, cart_id, quantity):
          self.authorize()
          print(cart_id, quantity)
          cart = Cart.query_by_cart_id(cart_id)
          
          cart:Cart = cart
          
          if quantity>=cart.quantity:
               cart.delete()
          else:
               cart.update_quantity(cart.quantity-quantity)
              
     def fetch_cart_products(self):
          self.authorize()
          
          user_id = self.session.user_id
          
          cart = CartObject.carts_to_objects(
               Cart.query_by_user_id(user_id)
          )
          
          products = []   
          for instance in cart:
               instance:CartObject = instance
               products.append(instance.product)        
          return products
 
     def fetch_cart(self, product_id):
          self.authorize()
          user_id = self.session.user_id
          return CartObject.cart_to_object(
               Cart.query_on_multiple_conditions(["user", "product"], [user_id, 
				product_id])[0])

     def fetch_orders(self):
          self.authorize()  
          user_id = self.session.user_id
          return OrderObject.orders_to_objects(
               Order.query_by_user_id(user_id)
          )
          
     def calculate_grand_total(self):
          self.authorize()
          user_id = self.session.user_id
          total = 0.0
          carts = CartObject.carts_to_objects(
               Cart.query_by_user_id(user_id)
          )
          


          for item in carts:
               item:CartObject = item
               total += item.quantity*item.product.price
          return total
     
     def checkout_cart(self, payment_method:TransactionMethod):
          self.authorize()
          cartobjects = CartObject.carts_to_objects(
               Cart.query_by_user_id(self.session.user_id)               
          )
          for cart_item in cartobjects:               
               cart_item:CartObject = cart_item
               product:ProductObject = cart_item.product
               vendor:UserObject = product.vendor
               
               tx = Transaction.new_instance(
                    user_id=self.session.user_id,
                    product_id=product.id,
                    quantity=cart_item.quantity,
                    amount=product.price*cart_item.quantity,
                    payment_method=payment_method
                    
               )
               tx.save()
                              
               Order.new_instance(
                    user_id=self.session.user_id,
                    vendor_id=vendor.user_id,
                    transaction=tx.id,
                    status=OrderStatus.PROCESSING
               ).save()
               
               Cart.query_by_cart_id(cart_item.cart_id).delete()


     def fetch_carts(self):
          ''' Fetches all Cart items for a particular user '''
          self.authorize()
          user_id = self.session.user_id
          return CartObject.carts_to_objects(
               Cart.query_by_user_id(user_id)
          )
          
     def update_address(self, address):
          self.authorize()
          User.query_by_id(self.session.user_id).update_address(address)
          self.session.address = address
          
     def update_first_name(self, first_name):
          self.authorize()
          User.query_by_id(self.session.user_id).update_first_name(first_name)
          self.session.first_name = first_name
          
     def update_last_name(self, last_name):
          self.authorize()
          User.query_by_id(self.session.user_id).update_last_name(last_name)
          self.session.last_name = last_name
          
     def update_email(self, email):
          self.authorize()
          User.query_by_id(self.session.user_id).update_email(email)
          self.session.email = email
          
     def update_telephone(self, telephone:int):
          self.authorize()
          User.query_by_id(self.session.user_id).update_telephone(telephone)
          self.session.telephone = telephone
          
     ''' Validates username for registration '''
     def validate_username(self, username):
          user = User.query_by_username(username)
          if user==None and len(username)>=4:
               return True
          return False
     
     def validate_address(self):
          self.authorize()
          if (self.session.address == None or self.session.address.strip()=="" or
               self.session.address.strip() == " " or len(self.session.address)<=5):
               return False

     def user_is_logged_in(self):
          if self.session == None:
               return False
          return True
          
     def authorize(self):
          # verifies if the user is logged in
          if not self.user_is_logged_in():
               raise Exception("User is not logged in")

     def logout(self):
          self.session = None
          
     def set_cookie(self, cookie:UserSession):
          self.session = cookie
          
class VendorService(object):
     def __init__(self, session:UserSession=None):
          self.session = session
     
     def fetch_orders(self):
          self.authorize()
          vendor_id = self.session.user_id
          
          return OrderObject.orders_to_objects(
               Order.query_by_vendor_id(vendor_id)
          )
          
     def fetch_products(self):
          self.authorize()
          vendor_id = self.session.user_id
          return ProductObject.products_to_objects(
               Product.query_by_vendor(vendor_id)
          )
          
     def change_status(self, order_id, status:OrderStatus):
          self.authorize()
          Order.query_by_id(order_id).update_status(status)
     
     def change_description(self, order_id, description):
          self.authorize()
          Product.query_by_id(order_id).update_description(description)

     def add_product(self, name, price, category, brand, description, stock):
          self.authorize()
          s:Product = Product.new_instance(name, category, price, brand, description, stock, 
		self.session.user_id)
          s.save()

     def update_stock(self, product_id, quantity):
          self.authorize()
          Product.query_by_id(product_id).update_stock(quantity)
     
     def user_is_logged_in(self):
          if self.session == None:
               return False
          return True

     
     def authorize(self):
          # verifies if the user is logged in
          if not self.user_is_logged_in():
               raise Exception("User is not logged in")

     def logout(self):
          self.session = None
     
     def set_cookie(self, cookie:UserSession):
          self.session = cookie
     
def login(username, password):
     user = User.query_by_username(username)
     if user==None:
          return None
     elif user.password == password:
          cookie = UserSession(user.user_id, user.username, user.type, user.email, user.address, user.telephone, user.first_name, user.last_name)
          return cookie
     else:
          return None
