from services.user import UserService,VendorService, login
from services.store import StoreService

from entities.product import ProductObject
from entities.user import UserType
from entities.tx import TransactionMethod
from entities.orders import OrderObject, OrderStatus
from entities.cart import CartObject

import tabulate

class ConsoleRunner:
     def __init__(self):
          self.user_service = UserService()
          self.vendor_service = VendorService()
          self.store_service = StoreService(
               name="E-Plaza",
               certificate='x-y-z certificate'
          )

     def run(self):
          try:
               self.render_start()
          except KeyboardInterrupt:
               s = input("\nAre you sure you want to exit.(Y/n)")
               if s.lower()=='y':
                    exit()
               else:
                    self.run()
          
     def render_start(self):
          choice = self.display_menu(["Login", "Register", "Forgot Password"], "Welcome to E-Plaza!")
          
          if choice == 1:
               self.render_login()
          elif choice == 2:
               self.render_register()
          elif choice == 3:
               self.render_forgot_password()

     def render_login(self):
          username = input("Username: ")
          password = input("Password: ")
          auth_cookie = login(username, password)
          if auth_cookie is None:
               print("Invalid username or password...")
               input("Press enter to continue...")
               self.render_start()
          else:
               print("Login Successful")
               if auth_cookie.type==UserType.VENDOR:
                    choice = self.display_menu(["Shop", "Manage"], "Vendor Menu")
                    if choice==0 or choice==3:
                         return self.render_start()
                    elif choice==2:
                         self.vendor_service.set_cookie(auth_cookie)
                         self.user_service.logout()
                         return self.render_vendor_page()
                    elif choice==1:
                         self.user_service.set_cookie(auth_cookie)
                         self.vendor_service.logout()
                         return self.render_home()
                    
               self.user_service.set_cookie(auth_cookie)
               self.render_home()
               
     def render_register(self):
          username = input("Username: ")
          if not self.user_service.validate_username(username):
               print("Invalid username")
               self.render_register()
          while True:
               email = input("Email: ")
               if email.find("@") == -1:
                    print("Invalid email")
               else:
                    break
          address = input("Address: ")
          while True:
               try:
                    telephone = int(input("Telephone: "))
                    if len(str(telephone))!=10:
                         print("Invalid telephone number")
                         continue
               except ValueError:
                    print("Invalid telephone number")
               else:
                    break
          first_name = input("First Name: ")
          last_name = input("Last Name: ")
          
          choice = self.display_menu(["Vendor", "Customer"], "Account Type")
          user_type = UserType.CUSTOMER
          if choice==0:
               return self.render_start()
          elif choice==1:
               user_type = UserType.VENDOR
          
          password = ''
          while True:
               password = input("Password: ")
               confirm_password = input("Confirm Password: ")               
               if password != confirm_password:
                    print("Passwords do not match. Please try again.")
                    continue  

               break  # Exit the loop when the passwords match
          response = self.user_service.register_customer(username, email, address, telephone, first_name, last_name, password, user_type)
          if response["status"]:
               print("Registration Successful")
               self.render_login()
          else:
               print("Registration Failed")
               print("Invalid fields: ", response["invalid_fields"])
               self.render_register()
     
     def render_forgot_password(self):
          username = input("Enter username: ")
          user = self.user_service.retrieve_user(username)
          if user is None:
               self.display_warning("User does not exist")
               input("Press enter to continue...")
               return self.render_start()
          
          while True:
               pass1 = input("Enter new password: ")
               pass2 = input("Confirm password: ")
               if pass1 == pass2:
                    break
          
          self.user_service.reset_password(username, pass1)
          self.display_info("Password reset successful. Please login with your new password")
          return self.render_start()
     
     def render_home(self):
          #  authorize only logged on users
          self.authorize()
          
          choice = self.display_menu(['Browse Products', 'My Cart', 'My Profile', 'My Orders', 'Logout'], 'Home Page')     
          if choice==1:
               self.render_browsing_page()
          elif choice==2:
               self.render_cart()
          elif choice==3:
               self.render_user_profile()
          elif choice==4:
               self.render_orders_page()
          else:
               self.user_service.logout()
               return self.render_start()
          
     # ---------------------------Browse-----------------------------
     def render_browsing_page(self):
          choice = self.display_menu(["All", "Browse By Category", "Browse By Name", 
				'Browse By Brand', 'Browse By Vendor'], "Browsing Page")          
          if choice == 1:
               self.render_browse_all()
          elif choice == 2:
               self.render_browse_by_category()
          elif choice == 3:
               self.render_browse_by_name()
          elif choice == 4:
               self.render_browse_by_brand()
          elif choice == 5:
               self.render_browse_by_vendor()
          elif choice == 0:
               return self.render_home()
          
     def render_browse_all(self):
          products = self.store_service.fetch_all_products()
          self.display_product_table(products)
          while True:
               choice = int(input("Enter the product: "))
               if choice >= 0 and choice <= len(products):
                    break
          
          if choice==0:
               return self.render_browsing_page()
          
          product = products[choice-1]
          self.render_product_page(product)
          
     def render_browse_by_category(self):
          categories = self.store_service.fetch_categories()
          choice = self.display_menu(categories, "Browse By Category")
          if choice==0:
               return self.render_browsing_page()
          category = categories[choice-1]
          category_products = self.store_service.fetch_products_by_category(category)
          
          if choice==0:
               return self.render_browsing_page()
          
          self.display_product_table(category_products)
          
          while True:
               choice = int(input("Enter the product: "))
               if choice >= 0 or choice < len(category_products):
                    break
          
          if choice==0:
               return self.render_browsing_page()
          
          product = category_products[choice-1]
          self.render_product_page(product)    
          
     def render_browse_by_name(self):
          print("-"*100)
          name = input("Enter the name of the product your searching for: ")
          print("-"*100)
          products = self.store_service.fetch_by_name(name)
          

          if len(products)==0:
               self.display_info("No products found")
               input("Press enter to continue...")
               return self.render_browsing_page()
          
          self.display_product_table(products)
          
          while True:
               choice = int(input("Enter the product: "))
               if choice >= 0 and choice <= len(products):
                    break
          if choice==0:
               return self.render_browsing_page()          
          product = products[choice-1]
          return self.render_product_page(product)
     
     def render_browse_by_brand(self):
          brands = self.store_service.fetch_brands()
          choice = self.display_menu(brands, "Browse By Brand")
          if choice==0:
               return self.render_browsing_page()
          brandname = brands[choice-1]
          products = self.store_service.fetch_by_brand(brandname)
          self.display_product_table(products=products)

          while True:
               choice = int(input("Enter the product: "))
               if choice >= 0 or choice < len(products):
                    break
          
          if choice==0:
               return self.render_browsing_page()
          
          product = products[choice-1]
          return self.render_product_page(product)
          
          
     def render_browse_by_vendor(self):
          print("-"*100)
          vendor = input("Enter the name of the vendor your searching for: ")
          print("-"*100)          
          products = self.store_service.fetch_by_vendor(vendor)
          if products == None or len(products)==0:
               self.display_info("No products found")
               input("Press enter to continue...")
               return self.render_browsing_page()
          self.display_product_table(products)
          
          while True:
               choice = int(input("Enter the product: "))
               if choice >= 0 or choice < len(products):
                    break
          
          if choice==0:
               return self.render_browsing_page()
          product = products[choice-1]
          return self.render_product_page(product)
     
               
     def render_product_page(self, product:ProductObject):
          self.display_product_details(
               product_id=product.id,
               name=product.name,
               description=product.description,
               vendor=product.vendor
          )
          if product.stock > 0:
               print(f"In stock")
          else:
               print("Out of stock")
               return self.render_browse_by_category()
               
          while True:
               choice = int(input("Enter 1 to add to cart, 0 to go back: "))
               if choice == 1:
                    try: 
                         quantity = int(input("Enter quantity: "))
                    except ValueError:
                         print("Enter a valid quantity")
                         continue
                    self.user_service.add_to_cart(product, quantity)
                    self.display_info(f"Added {quantity} {product.name} to cart")
                    return self.render_browsing_page()
               elif choice == 0:
                    return self.render_browsing_page()
          
     # ------------------------------------------------
     
     def render_cart(self):
          self.authorize()
          products = self.user_service.fetch_carts()    
          if len(products)==0:
               self.display_info("Cart is empty")
               input("Press enter to continue...")
               return self.render_home()
           
          self.display_cart_table(products)
          self.display_grand_total(self.user_service.calculate_grand_total())
          
          choice = self.display_menu(["Checkout", "Continue Shpping", "Remove Items"],
				"Cart Page")
          if choice==0:
               return self.render_home()
          elif choice==1:
               return self.render_billing_page()
          elif choice==2:
               return self.render_browsing_page()
          elif choice==3:
               self.render_remove_cart_items()
               
     def render_remove_cart_items(self):
          products = self.user_service.fetch_cart_products()
          while True:
                    try:
                         choice = int(input("Enter the number of the item you want to remove: "))
                         
                         if choice==0:
                              return self.render_cart()
                         elif choice<0 or choice>len(products):
                              print("Enter a valid number")
                              continue
                         item = products[choice-1]
                         cartobj:CartObject = self.user_service.fetch_cart(item.id)
                         
                         qty = int(input("Enter the quantity you want to remove: "))
                         if choice==0:
                              self.render_cart()
                         if qty>=cartobj.quantity:
                              initial_qty = cartobj.quantity
                              self.display_warning(f"There are only {cartobj.quantity} {item.name}s in cart\nAre you sure you want remove them all? (y/n)")
                              choice = input()
      
                              if choice.lower()=='y':
                                   self.user_service.remove_from_cart(cartobj.cart_id, qty)
                                   self.display_info(f"Removed {initial_qty} {item.name} from cart")
                                   return self.render_cart()

                              else:
                                   continue
                         else:
                              self.user_service.remove_from_cart(cartobj.cart_id, qty)
                              self.display_info(f"Removed {qty} {item.name} from cart")
                              return self.render_cart()
                              
                    except ValueError:
                         print("Enter a valid number")
                         continue
               
                              
     def render_user_profile(self):
          address = self.user_service.session.address
          email = self.user_service.session.email
          first_name = self.user_service.session.first_name
          last_name = self.user_service.session.last_name
          telephone = self.user_service.session.telephone
          username = self.user_service.session.username
          user_type = self.user_service.session.type
          
          user_data = [
               ["Address", address],
               ["Email", email],
               ["First Name", first_name],
               ["Last Name", last_name],
               ["Telephone", telephone],
               ["Username", username],
               ["Account Type", user_type],
          ]          
          
          print(tabulate.tabulate(user_data, headers=["Field", "Value"], tablefmt="grid"))
          choice = self.display_menu(["Update Profile", "Back"], "Profile")
          

          if choice==0 or choice==2:
               return self.render_home()
          elif choice==1:
               option = self.display_menu(["Update Address", "Update Email", 
			"Update First Name", "Update Last Name", "Update Telephone"], 
			"Update Profile")
               
               if option==1:
                    address = input("Enter Address: ")
                    self.user_service.update_address(address)
               elif option==2:
                    email = input("Enter Email: ")
                    self.user_service.update_email(email)
               elif option==3:
                    first_name = input("Enter First Name: ")
                    self.user_service.update_first_name(first_name)
               elif option==4:
                    last_name = input("Enter Last Name: ")
                    self.user_service.update_last_name(last_name)
               elif option==5:
                    while True:
                         try: 
                              telephone = int("Enter telephone: ")
                              
                              self.user_service.update_telephone(telephone)
                         except ValueError:
                              print("Enter a valid number")
                              continue
                         
          return self.render_user_profile()       
     
     def render_orders_page(self):
          self.display_orders(self.user_service.fetch_orders())
          input("Press enter to continue...")
          self.render_home()
     
     def render_billing_page(self):
          
          carts = self.user_service.fetch_carts()
          
          self.display_bill(carts)
          self.display_grand_total(self.user_service.calculate_grand_total())
          
          option = self.display_menu(["Proceed to Payment", "Back"], "Billing")
          
          if option == 0 or option==2:
               self.render_cart()
          elif option == 1:
               if self.user_service.validate_address()==False:
                    self.display_warning("Invalid Address. Please update your address and credentials for delivery...")
                    input("Press enter to continue...")
                    return self.render_user_profile()
               self.render_confirm_billing()
          
     def render_confirm_billing(self):
          grand_total = self.user_service.calculate_grand_total()
          
          choice = self.display_menu(["Pay with Credit Card", "Pay with Debit Card", 
				"Pay with Bank Transfer", "Pay with Cash", 'UPI'], 
				"Payment Method")
          if choice==0:
               self.render_cart()
          method =  TransactionMethod.UPI
          if choice==1:
               method = TransactionMethod.ONLINE_BANKING
          elif choice==2:
               method = TransactionMethod.ONLINE_BANKING
          elif choice==3:
               method = TransactionMethod.ONLINE_BANKING
          elif choice==4:
               method = TransactionMethod.CASH_ON_DELIVERY
          
          while True:
               password = input("Enter your password: ")     
               flag = self.user_service.authenticate(password)
               if flag==True:
                    break
               else:
                    print("Incorrect password. Please try again.")
                    self.render_billing_page()
          
          choice = self.display_menu(["Confirm Billing", "Back"], "Confirm Billing")
          
          if choice == 0 or choice==2:
               return self.render_cart()
          elif choice == 1:
               self.user_service.checkout_cart(method)
               self.display_info("Billing Successful")
               return self.render_home()
               
     # ----------------------VENDOR-PAGE------------------------
     def render_vendor_page(self):
          choice = self.display_menu(["Orders", "Update Stock", "Products", "Logout"],
				"Vendor Management")
          
          if choice==1:
               return self.render_vendor_orders_page()
          elif choice==2:
               return self.render_vendor_update_stock_page()
          elif choice==3:
               return self.render_vendor_add_product_page()
          elif choice==4:
               return self.logout()
          # TODO: Impl. all vendor feat.
          
     def render_vendor_orders_page(self):
          orders = self.vendor_service.fetch_orders()
          self.display_vendor_orders(orders)
          choice = self.display_menu(["Change Status","Back"], "Your Orders")
          
          if choice==1:
               return self.render_change_status(orders)
          elif choice==2 or 0:
               return self.render_vendor_page()
               
     def render_change_status(self, orders:list[OrderObject]):
          while True:
                    try:
                         val = int(input("Enter the number for which order you want to change status: "))
                         order = orders[val-1]
                         
                         choice = self.display_menu(["Processing", "Shipped",
					"Out for delivery", "Cancelled", "Returned", "Delivered"], 
					"Update Status")
                         
                         if choice==1:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.PROCESSING)
                         elif choice==2:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.SHIPPED)
                         elif choice==3:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.OUT_FOR_DELIVERY)
                         elif choice==4:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.CANCELLED)

                         elif choice==5:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.RETURNED)
                         elif choice==6:
                              self.vendor_service.change_status(order.id, 
						OrderStatus.DELIVERED)
                         else:
                              self.render_vendor_orders_page()
                    except ValueError:
                         print("Enter a valid number")
                         continue
                    break 
          self.display_info("Status updated successfully")
          input("Press enter to continue...")
          return self.render_vendor_orders_page()
     
     def render_vendor_update_stock_page(self):
          products = self.vendor_service.fetch_products()
          self.display_vendor_stock(products)
          
          while True:
               choice = int(input("Enter the product: "))
               product = products[choice-1]
               
               quantity = int(input("Enter the quantity: "))
               
               self.vendor_service.update_stock(product.id, quantity)
               self.display_info("Stock updated successfully")
               input("Press enter to continue...")
               if choice >= 0 and choice <= len(products):
                    break
               else:
                    print("Enter a valid number")
          return self.render_vendor_page()
          
     def render_vendor_add_product_page(self):
          products = self.vendor_service.fetch_products()
          
          self.display_vendor_stock(products)
          
          choice = self.display_menu(["Add Product", "Change Description"],
				'Product Dashboard')          
          if choice==0 or choice==3:
               return self.render_vendor_page()
          elif choice==1:
               while True:
                    try:
                         name = input("Enter product name: ")
                         price = float(input("Enter product price: "))
                         categories = self.store_service.fetch_categories()
                         choice = self.display_menu(categories, "Category")
                         prod_category = categories[choice-1]
                         
                         brand = input("Enter product brand: ")
                         description = input("Enter product description: ")
                         stock = int(input("Enter product stock: "))
                         self.vendor_service.add_product(name, price, prod_category, brand, 
						description, stock)
                         break
                    except ValueError:
                         print("Enter a valid number")
               self.display_info("Product added successfully")
                         
          elif choice==2:
               while True:
                    try:
                         val = int(input("Enter the number for which product you want to change description: "))
                         product = products[val-1]
                         description = input("Enter new description: ")
                         self.vendor_service.change_description(product.id, description)
                         break
                    except ValueError:
                         print("Enter a valid number")
                         continue
               self.display_info("Description updated successfully")
          input("Press enter to continue...")
          return self.render_vendor_page()
     
     def logout(self):
          pass     
     # ------------------Utilities------------------------------
     def display_menu(self, options, header):
          while True:
               # Calculate the maximum length for the options
               max_option_length = max(len(str(option)) for option in options)
               # Print the header
               header_line = f"======== {header} ========"
               print("="*len(header_line))
               print(header_line)
               print("="*len(header_line))
               
               # Print each option
               for i, option in enumerate(options, start=1):
                    print(f"{i}. {option}")

               # Print the exit option
               print(f"{len(options) + 1}. Exit")
               
               print("="*len(header_line))
               try:     
                    value = int(input("Enter your choice: "))
                    if value < 0 or value > len(options)+1:
                         raise ValueError
               except ValueError:
                    print("Enter a valid option")
               else:
                    break
          return value
     
     def display_cart_table(self, products:list[CartObject]):
          # Prepare data for tabulate
          table = [(i + 1,p.product.brand, p.product.name, f"₹{p.product.price:.2f}", p.product.category, p.quantity, p.quantity*p.product.price) for i, p in enumerate(products)]
          # Print the table
          print(tabulate.tabulate(table, headers=["No.","Brand", "Product Name","Price (INR)", "Category", 'Quantity', 'Total'], tablefmt="grid"))
          
     def display_product_table(self, products:list[ProductObject]):
          # Prepare data for tabulate
          table = [(i + 1,p.brand, p.name, p.category,p.vendor, p.description) for i, p in enumerate(products)]
          # Print the table
          print(tabulate.tabulate(table, headers=["No.","Brand", "Product Name",  "Category", 'Vendor', 'Description'], tablefmt="grid"))
          
     def authorize(self):
          if not self.user_service.user_is_logged_in():
               message = "Login First"
               print("-"*len(message))
               print(message)
               print("-"*len(message))
               return self.render_start()

     def display_info(self,message):
          # ANSI code for blue text
          BLUE = '\033[34m'
          # ANSI code to reset to default
          RESET = '\033[0m'
          print(f"{BLUE}[INFO]{RESET} {message}")

     def display_warning(self, message):
          # ANSI code for yellow text
          YELLOW = '\033[33m'
          # ANSI code to reset to default
          RESET = '\033[0m'
          print(f"{YELLOW}[WARNING]{RESET} {message}")
          
     def display_product_details(self, product_id, name, description, vendor):
          # Print the header with underline
          print(f"{'PRODUCT DETAILS':^50}")
          print("=" * 50)

          # Print the details in a formatted way
          print(f"{'ID':<15}: {product_id}")
          print(f"{'Name':<15}: {name}")
          print(f"{'Description':<15}: {description}")
          print(f"{'Vendor':<15}: {vendor.username}")

          # Footer for separation
          print("=" * 50)
          
     def display_grand_total(self, grand_total):
          total_str = f" Grand Total: ₹{grand_total:.2f} "
          border = "+" + "-" * (len(total_str) + 2) + "+"
          print("\033[1;32m" + border)
          print(f"| {total_str} |")
          print(border + "\033[0m")          

     def display_bill(self, carts:list[CartObject]):
          table = [(i+1, p.product.name, p.product.price,
			p.quantity,f'₹{p.quantity*p.product.price:.2f}')
			for i, p in enumerate(carts)]

          print(tabulate.tabulate(table, headers=["No.", "Product Name", "Price", 
				"Quantity", "Total"], tablefmt="grid"))
          

     def display_orders(self, orders:list[OrderObject]):
          table = [(i+1, p.transaction.item.name, 
				p.transaction.quantity,f'₹{p.transaction.price:.2f}', 
				p.vendor.username, p.status)for i, p in enumerate(orders)]
          print(tabulate.tabulate(table, headers=["No.", "Product Name", "Quantity", 
				"Price", "Vendor", "Status"], tablefmt="grid"))
          
     def display_vendor_orders(self, orders:list[OrderObject]):
          table = [(i+1, p.transaction.item.name,
			p.transaction.quantity,f'₹{p.transaction.price:.2f}',p.status,
                    p.transaction.user.address,p.transaction.user.username,
                    p.transaction.user.telephone, p.transaction.user.first_name,
                    p.transaction.user.email )for i, p in enumerate(orders)]
          print(tabulate.tabulate(table, headers=["No.", "Product Name", "Quantity", 
				"Price", "Status", "Address", "Username", "Telephone",
				"First Name", "Email"], tablefmt="grid"))
          
     def display_vendor_stock(self, products:list[ProductObject]):
          table = [(i+1, p.brand, p.name, p.category, p.price, p.stock, p.description)
				for i, p in enumerate(products)]
          print(tabulate.tabulate(table, headers=["No.", "Brand", "Product Name", 
				"Category", "Price", "Stock", "Description"], tablefmt="grid"))
