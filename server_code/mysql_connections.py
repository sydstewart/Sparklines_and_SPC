import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server

import pymysql
 
def connect():
  
  connection = pymysql.connect(host='51.140.44.126',
                               port=3306,
                               user='root',
                               password=anvil.secrets.get_secret('4s-mysql'),
                               cursorclass=pymysql.cursors.DictCursor)
  
  if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
  return connection

@anvil.server.callable
def get_cases():
  conn = connect()

  with conn.cursor() as cur:
    cur.execute("Select  cases.date_entered as Date_Entered from cases")
    return cur.fetchall()
