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
  connection = pymysql.connect(host='192.168.0.217',
                               port=3306,
                               user='CRMReadOnly',
                               password=anvil.secrets.get_secret('db_password'),
                               cursorclass=pymysql.cursors.DictCursor)
  return connection

@anvil.server.callable
def get_people():
  conn = connect()
  with conn.cursor() as cur:
    cur.execute("SELECT name,date_of_birth,score FROM users")
    return cur.fetchall()
#

