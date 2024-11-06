
import mysql.connector as mysql_connector

class SubstringType:
     END = 'end'
     START = 'start'
     BETWEEN = 'between'

class Repository:
     def __init__(self, host:str, user:str, password:str, database:str):
          # variable initialization
          self.host = host
          self.user = user
          self.password = password
          self.database = database
          
          # establishing connection to database
          try:
               self.connection = mysql_connector.connect(
                    host = self.host,
                    user = self.user,
                    password = self.password,
                    database = self.database
               )
          except Exception as e:
               raise Exception("Could not connect to database: " + str(e))
             
     def new_instance(self, connection):
          self.connection = connection
          return self
     
     def query_all(self, table:str):
          cursor = self.connection.cursor()
          cursor.execute(f"SELECT * FROM {table}")
          return cursor.fetchall()
     

     def query_one(self, table:str, column, value):
          cursor = self.connection.cursor()
          cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")
          return cursor.fetchone()
     
     def query(self, table:str, column, value):
          cursor = self.connection.cursor()
          cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")
          return cursor.fetchall()
     
     def new_entry(self, table:str, columns:list, values:list):
          cursor = self.connection.cursor()
          
          for i in range(len(values)):
               if type(values[i]) == int or type(values[i]) == float:
                    values[i] = str(values[i])
          cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})")
          self.connection.commit()
          return cursor.lastrowid
          
     
     def alter_entry(self, table: str, columns: list, values: list, cond_column: str, cond_value: str):
          cursor = self.connection.cursor()
          
          # Constructing the SET clause
          set_clause = ", ".join([f"{col} = %s" for col in columns])
          
          # Creating the SQL query
          query = f"UPDATE {table} SET {set_clause} WHERE {cond_column} = %s"
          
          # Prepare the values to be passed (no need to convert)
          params = values + [cond_value]

          try:
               # Executing the query with parameters
               cursor.execute(query, params)
               self.connection.commit()
               print("Entry updated successfully")
          except Exception as e:
               print(f"Error updating entry: {e}")
          finally:
               cursor.close()
     
     def query_distinct(self, table: str, column: str):
          cursor = self.connection.cursor()
          cursor.execute(f"SELECT DISTINCT {column} FROM {table}")
          return cursor.fetchall()     
     
     def query_on_multiple_conditions(self, table, columns:list, values:list):
          cursor = self.connection.cursor()
          query = f'''SELECT * FROM {table} WHERE '''
          
          assert len(columns) == len(values)
          
          for i in range(len(columns)):
               query += f"{columns[i]} = {values[i]}"
               
               if i < len(columns) - 1:
                    query += " AND "
          
          query += " ;"
          
          cursor.execute(query)
          return cursor.fetchall()
          
     def query_enum_types(self, table, column):
          cursor = self.connection.cursor()
          query = f'''SHOW COLUMNS FROM {table} LIKE {column}'''
          cursor.execute("SHOW COLUMNS FROM product LIKE 'category';")
          data = cursor.fetchall()
          return data[0][1][5::].replace("'","").replace(")","").split(",")
     
     def query_substring(self, table: str, column: str, substring: str, type:SubstringType):
          query = f'''SELECT * FROM {table}
                    WHERE {column} LIKE'''
                    
          if type == SubstringType.END:
               query += f" '%{substring}';"
          elif type == SubstringType.START:
               query += f" '{substring}%';"
          elif type == SubstringType.BETWEEN:
               query += f" '%{substring}%';"
          
          cursor = self.connection.cursor()
          cursor.execute(query)
          return cursor.fetchall()
          
     def delete(self, table:str, column, value):
          cursor = self.connection.cursor()
          cursor.execute(f"DELETE FROM {table} WHERE {column} = '{value}'")
          self.connection.commit()
     
     def close(self):
          self.connection.close()
     
     def is_connected(self):
          return self.connection.is_connected()
     
     def execute(self, query):
          cursor = self.connection.cursor()
          cursor.execute(query)
          return cursor.fetchall()
