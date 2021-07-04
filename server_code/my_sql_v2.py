import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import requests
import json
import pandas as pd
import anvil.media
from datetime import datetime ,timedelta, date
from io import BytesIO
import numpy as np
import io
import plotly.graph_objects as go
from anvil import tz

@anvil.server.callable
def convert_dict(dict, offset):
  import pandas as pd
  Organisation = app_tables.organisation.get(id = 1)
  df = pd.DataFrame().append(dict, ignore_index=True)
  print(df)
  df_as_csv = df.to_csv(index=False)
#     print(df)
  ticker = 'demo'
  filename = ticker +'.csv' 
  csv_bytes = bytes(df_as_csv, 'utf-8') # fix  
  m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name=filename)
  


  file_row = app_tables.my_files.get(name=filename)
  client = tz.tzoffset(seconds=offset)
  now = datetime.now(client)
  
  if file_row != None:
    file_row["media_obj"] = m 
    file_row["last_uploaded"] = now
#       alert('File updated')
  else:
#       alert('File does not exist - adding new file')
    app_tables.my_files.add_row(
    name=filename, 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now )
  
# import pymysql.cursors

# @anvil.server.callable  
# def mysql_access():
#   connection = pymysql.connect(host='192.168.0.217',
#                               port=3306,
#                               user='tableau',
#                               password=None,
#                               database='infoathand')
#   return connection

# @anvil.server.callable
# def TestConnection():
#   conn = anvil.server.call('mysql_access')
#   print(conn)
                               
                               
#     connection=pymysql.connect(
#           host="192.168.0.217",
#           user="root",
#           password="root",
#           port=3306, # 3306 is standard & default so you can omit this.
#           db="infoathand",
#           cursorclass=pymysql.cursors.DictCursor
#         )
    
#     with connection.cursor() as cursor:
#         connection.execute("SELECT * FROM cases Where Date(cases.date_entered) >=   '2021-07-01'")
#         result = connection.fetchall()
#         print(result) # python 3 print syntax
#         return result


# @anvil.server.callable
# def say_hello():
#    cases_Summary = mysql_access()

#    anvil.server.wait_forever()    