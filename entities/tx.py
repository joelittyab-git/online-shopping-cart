from data import create_default_repo
from .user import UserObject,User
from .product import Product,ProductObject

from datetime import datetime

class TransactionMethod:
     CASH_ON_DELIVERY = 'cash_on_delivery'
     ONLINE_BANKING = 'online_banking'
     UPI = 'upi'
     
     def parse(method):
          if method == 'cash_on_delivery':
               return TransactionMethod.CASH_ON_DELIVERY
          if method == 'online_banking':
               return TransactionMethod.ONLINE_BANKING
          if method == 'upi':
               return TransactionMethod.UPI


class Transaction(object):
     def __init__(self, tx_id, user_id, product_id, date, payment_method:TransactionMethod, amount, quantity):
          self.tx_id = tx_id
          self.user_id = user_id   
          self.product_id = product_id
          self.date = date
          self.payment_method = payment_method
          self.amount = amount
          self.quantity = quantity
          
     def new_instance(user_id, product_id, payment_method:TransactionMethod, amount, quantity):
          return Transaction(0, user_id, product_id,datetime.now(), payment_method, amount, quantity)
          
     def save(self):
          repo = create_default_repo()
          new_id = repo.new_entry("transaction", ["user", "item", "payment_method", "price", "quantity"], [self.user_id, self.product_id, f"'{self.payment_method}'", self.amount, self.quantity])
          self.id = new_id
          repo.close()
     
     def query_instance(column, value):
          repo = create_default_repo()
          
          data = repo.query_one("transaction", column, value)
          repo.close()
          
          return Transaction._to_transaction(data)
     
     def query_all():
          repo = create_default_repo()
          data =  repo.query_all("transaction")
          repo.close()

          tx_list = []
          for tx in data:
               tx_list.append(Transaction._to_transaction(tx))          
          return tx_list
     
     def delete(self):
          repo = create_default_repo()
          repo.delete("transaction", "tx_id", str(self.tx_id))
          repo.close()
          



     def query_all_instances(column, value):
          repo = create_default_repo()          
          data =  repo.query("transaction",column, value)
          repo.close()
          
          tx_list = []
          for tx in data:
               tx_list.append(Transaction._to_transaction(tx))
          return tx_list
     
     '''------------------FETCH-QUERY-------------------'''
     def query_by_id(id):
          return Transaction.query_instance("tx_id", id)
     
     def query_by_user_id(user_id):
          return Transaction.query_all_instances("user", user_id)
     
     def query_by_product_id(product_id):
          return Transaction.query_all_instances("item", product_id)
     
     def query_by_date(date):
          return Transaction.query_all_instances("date", date)
     
     def query_by_payment_method(payment_method):
          return Transaction.query_all_instances("payment_method", payment_method)
     
     def query_by_amount(amount):
          return Transaction.query_all_instances("price", amount)
     
     '''------------------UPDATE-QUERY-------------------'''
     
     def update(self, field, value):
          repo = create_default_repo()
          repo.alter_entry("transaction", [field], [value], "tx_id", str(self.tx_id))
          repo.close()
     
     def update_user_id(self, user_id):
          self.user_id = user_id          
          self.update("user_id", self.user_id)
          
     def update_product_id(self, product_id):
          self.product_id = product_id          
          self.update("item", self.product_id)
          
     def update_date(self, date):
          self.date = date
          self.update("date", self.date)
          
     def update_payment_method(self, payment_method):
          self.payment_method = payment_method          
          self.update("payment_method", self.payment_method)
          
     def update_amount(self, amount):
          self.amount = amount          
          self.update("price", self.amount)
     
     def _to_transaction(data):
          if data==None:
               return None
          
          payment_method = 'cash_on_delivery'
          if data[4] == 'online_banking':
               payment_method = 'online_banking'
          if data[4] == 'upi':
               payment_method = 'upi'
          return Transaction(data[0],data[1],data[2],data[3],payment_method,data[5], data[6])
     
     


class TransactionObject:
     def __init__(self, tx_id, user_obj:UserObject, product_obj:ProductObject, date, payment_method:TransactionMethod, price, quantity):
          self.tx_id = tx_id
          self.user = user_obj
          self.item = product_obj
          self.date = date
          self.price = price
          self.payment_method = payment_method
          self.quantity = quantity
          
     def parse(data):
          if data == None:
               return data
          user_obj = User.query_by_id(data[1])
          payment_method = TransactionMethod.parse(data[4])
          
          return TransactionObject(data[0],user_obj,data[2],data[3],
		payment_method,data[5],data[6])
     
     def transaction_to_object(data:Transaction):
          if data == None:
               return data   
          # parsing user id to user obejct
          user = User.query_by_id(data.user_id)
          user_obj = UserObject.user_to_object(user)
          
          # parsing product id to product object
          product = Product.query_by_id(data.product_id)
          product_object = ProductObject.product_to_object(product)
          tx_method = TransactionMethod.parse(data.payment_method)
          return TransactionObject(data.tx_id,user_obj,product_object,data.date,
		tx_method,data.amount, data.quantity)
