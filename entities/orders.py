from data import create_default_repo

from .user import User, UserObject
from .tx import Transaction, TransactionObject

from datetime import datetime

class OrderStatus:
     PROCESSING = 'processing'
     SHIPPED = 'shipped'
     OUT_FOR_DELIVERY = 'out_for_delivery'
     CANCELLED = 'cancelled'
     RETURNED = 'returned'
     DELIVERED = 'delivered'
     
     
class Order:
     def __init__(self, id, user_id, vendor_id, transaction,status):
          self.id = id
          self.status = status
          self.user_id = user_id
          self.vendor_id = vendor_id
          self.transaction = transaction
          self.status = status
        
        
        
     def new_instance(user_id, vendor_id, transaction, status):
         return Order(0, user_id, vendor_id, transaction, status)
    
    


     def save(self):
          repo = create_default_repo()
          new_id = repo.new_entry("orders",
                    ["user", "vendor", "transaction", "status"],
                    [self.user_id, self.vendor_id, self.transaction, f"'{self.status}'"])
          self.id = new_id
          repo.close()
          
     def query_instance(column, value):
          repo = create_default_repo()
          
          data = repo.query_one("orders", column, value)
          repo.close()
          
          return Order._to_order(data)
     
     
     def query_all():
          repo = create_default_repo()
          
          data = repo.query_all("orders")
          repo.close()
          
          orders_list = []
          
          for i in data:
               pr = Order._to_order(i)
               orders_list.append(pr)
          
          return orders_list
     
     def delete(self):
          repo = create_default_repo()
          repo.delete("orders","order_id", self.id)
          repo.close()
          
     def query_all_instances(column, value):
          repo = create_default_repo()
          
          data = repo.query("orders", column, value)
          repo.close()
          
          orders_list = []
          
          for i in data:
               pr = Order._to_order(i)
               orders_list.append(pr)
          
          return orders_list
     
     
     def query_by_id(id):
          return Order.query_instance("order_id", id)
     
     def query_by_user_id(user_id):
          return Order.query_all_instances("user", user_id)
     
     def query_by_vendor_id(vendor_id):
          return Order.query_all_instances("vendor", vendor_id)
     
     def query_by_transaction(transaction):
          return Order.query_all_instances("transaction", transaction)
     
     def query_by_status(status):
          return Order.query_all_instances("status", status)
     
     
     def update_status(self, status:OrderStatus):
          self.status = status
          repo = create_default_repo()
          
          repo.alter_entry("orders", ["status"], [self.status], "order_id", str(self.id))
          
          
     
     def _to_order(data):
          if data==None:
               return data
          
          return Order(data[0], data[1], data[2], data[3], data[4])

class OrderObject:
     def __init__(self, id, user, vendor, transaction, status):
          self.id = id
          self.user = user
          self.vendor = vendor
          self.transaction = transaction
          self.status = status
          
     def parse(data):
          if data == None:
               return data
          
          return OrderObject(data[0], data[1], data[2], data[3], data[4])
     
     def order_to_object(data:Order):
          
          if data == None:
               return data
          
          user = User.query_by_id(data.user_id)
          user_obj = UserObject.user_to_object(user)
          
          vendor = User.query_by_id(data.vendor_id)
          vendor_obj = UserObject.user_to_object(vendor)
          
          transaction = Transaction.query_by_id(data.transaction)
          transaction_obj = TransactionObject.transaction_to_object(transaction)
          
          return OrderObject(data.id, user_obj, vendor_obj, transaction_obj, data.status)
     
     def orders_to_objects(data:list[Order]):
          if data == None:
               return data
        
          order_list = []
          
          for i in data:
               order_list.append(OrderObject.order_to_object(i))
          
          return order_list
