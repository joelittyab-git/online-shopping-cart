
from data import create_default_repo
from data.database import SubstringType

class UserType:
     VENDOR = "vendor"
     CUSTOMER = "customer"
     

class User:
     def __init__(self, user_id, username, email, type:UserType, address, telephone, first_name, last_name, password):   
          self.user_id = user_id
          self.username = username
          self.email = email
          self.type = type
          self.address = address
          self.telephone = telephone
          self.first_name = first_name
          self.last_name = last_name
          self.password = password
          
          
     def new_instance(username, email, type, address, telephone, first_name, last_name, 
			password):
          return User(0, username, email, type, address, telephone, first_name, last_name, 
     			password)
     def save(self):
          repo = create_default_repo()
          # Defaults to customer
          t = "customer"
          if self.type == UserType.VENDOR:
               t = "vendor"
          elif self.type == UserType.CUSTOMER:
               t = "customer"
          
          
          # Potentential issue: The user telephone is bracketed with quotes
          repo.new_entry("user",
               ["username", "email", "type", "address", "telephone", 
			"first_name","last_name","password"],
               ["'"+self.username+"'", "'"+self.email+"'", "'"+t+"'", "'"+self.address+"'", 
			f"'{self.telephone}'", "'"+self.first_name+"'", "'"+self.last_name+"'",
"'"+self.password+"'"]
          )
          repo.close()
          
          
     def query_instance(column, value):
          repo = create_default_repo()
          d = repo.query_one("user", column, value)
          repo.close()
          return User._to_user(d)
     
     def query_all():
          repo = create_default_repo()
          d = repo.query_all("user")
          repo.close()
          
          userobj_list = []
          for i in d:
               userobj_list.append(User._to_user(i))
          return userobj_list
     
     def query_all_instances(column, value):
          repo = create_default_repo()
          d = repo.query("user", column, value)
          repo.close()
          
          userobj_list = []
          
          for i in d:
               userobj_list.append(User._to_user(i))
          
          return userobj_list
     
     '''------------------FETCH-QUERY-------------------'''
     def query_by_username(username):
          return User.query_instance("username", username)
     
     def query_by_email(email):
          return User.query_all_instances("email", email)
     
     def query_by_id(id):
          return User.query_instance("user_id", id)
     
     def query_by_telephone(telephone):
          return User.query_all_instances("telephone", telephone)
     
     def query_by_first_name(first_name):
          return User.query_all_instances("first_name", first_name)
     
     def query_by_last_name(last_name):
          return User.query_all_instances("last_name", last_name)
     
     def query_by_type(type:UserType):
          return User.query_all_instances("type", type)
     
     ''''''
     def query_by_vendor_name_substring(substring):
          repo = create_default_repo()
          
          data = repo.query_substring(
               table="user", 
               column="username", 
               substring=substring, 
               type=SubstringType.BETWEEN
          )
          repo.close()

          user_list = []          
          for user in data:
               if user[3]==UserType.VENDOR:
                    u = User._to_user(user)
                    user_list.append(u)
          return user_list
     
          
     '''------------------UPDATE-QUERY-------------------'''
     
     def update(self, field, value):
          repo = create_default_repo()          
          repo.alter_entry("user", [field], [value], "user_id", self.user_id)          
          repo.close()
     
     def update_username(self, username):
          self.update("username", "'"+username+"'")
          self.username = username

     def update_email(self, email):
          self.update("email",email)
          self.email = email
          
     def update_password(self, password):
          self.update("password",password)
          self.password = password
          
     def update_address(self, address):          
          self("address",address)  
          self.address = address
          
     def update_telephone(self, telephone):
          self.update("telephone", telephone)
          self.telephone = telephone
          
     def update_first_name(self, first_name):
          self.update("first_name", first_name)
          self.first_name = first_name          
          
     def update_last_name(self, last_name):
          self.update("last_name", last_name)
          self.last_name = last_name
          
     def _to_user(data):
          if data==None:
               return None
          user_type = UserType.CUSTOMER
          if data[3] == "vendor":
               user_type = UserType.VENDOR
          return User(data[0],data[1],data[2],user_type,data[4],
		data[5],data[6],data[7],data[8])
     
     
class UserObject:
     def __init__(self, user_id, username, email, type:UserType, address, telephone,
		first_name, last_name, password):
          self.user_id = user_id
          self.username = username
          self.email = email
          self.type = type
          self.address = address
          self.telephone = telephone
          self.first_name = first_name
          self.last_name = last_name
          self.password = password

     '''Converts a database query output to an object'''
     def parse(itterable):
          if itterable == None:
               return itterable
          
          return UserObject(
               itterable[0],
               itterable[1],
               itterable[2],
               itterable[3],
               itterable[4],
               itterable[5],
               itterable[6],  
               itterable[7],
               itterable[8]
          )
          
     def user_to_object(user):
          if user == None:
               return None
          return UserObject(user.user_id, user.username, user.email, user.type,     
		user.address, user.telephone, user.first_name, user.last_name, user.password)

     def users_to_objects(users):
          if users == None:
               return None
          return [UserObject(user.user_id, user.username, user.email, user.type, user.address, user.telephone, user.first_name, user.last_name,user.password) for user in users]
