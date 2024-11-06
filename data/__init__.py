from .database import Repository

def create_default_repo()->Repository:
     """
     Initializes and returns a Repository instance connected to the specified MySQL database.
          
     This function establishes a connection to the MySQL database using predefined connection 
     parameters. The connection details (host, user, password, database) are hardcoded 
     for this instance.

     Returns:
          Repository: An instance of the Repository class, connected to the 
          'online_shopping_cart' database on the MySQL server running on localhost.

     Raises:
          Exception: If the connection to the database cannot be established, 
          an exception will be raised indicating the error encountered.
     """
     return Repository(
          host = "localhost",
          user = "root",
          password = "Tiger@123",
          database = "online_shopping_cart_test"
     )     

