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
from datetime import datetime, timedelta, timezone, date
from anvil import tz
from io import BytesIO
import numpy as np
import io
import plotly.graph_objects as go


@anvil.server.callable  
def get_RH_statcounter(offset):
  from datetime import timezone
  import xml.etree.ElementTree as ET
  
  dt = datetime.now()
  timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
  print(int(timestamp))
  query = 'http://api.statcounter.com/stats/'
  version = '?vn=3'
  visitor = '&s=summary'
  formats = '&f=json'
  projectid = '&pi=3364593'
#   projectid = '&pi=2292634'
  numberofresults ='&n=5'
  timeofquery = '&t='+ str(int(timestamp))
  username = '&u=sydstewart' 
#   username = '&u=demo_user'
  apipassword  = 'Arnside2021'
#   apipassword  = 'statcounter'
  startyear = '&g=daily&sd=01&sm=01&sy=20190&ed=31&em=5&ey=2021'
#   Username: demo_user
# API Password: statcounter
# Demo Project ID: 2292634
  sha1query =version + visitor + formats + projectid + startyear + timeofquery + username + apipassword 
  print(sha1query)
  myhash = SH1Hash(sha1query)
  myhash = '&sha1=' + myhash
  apiquery = version + visitor + formats + projectid + startyear + timeofquery + username + myhash
  print (myhash)
  print (apiquery)
  finalquery = query + version + visitor + formats + projectid  + startyear + timeofquery + username + myhash
  print(finalquery)
  
  
#   http://api.statcounter.com/stats/?vn=VERSION_NUMBER&s=summary&g=GRANULARITY&sd=START_DAY&sm=START_MONTH&sy=START_YEAR&ed=END_DAY&em=END_MONTH&ey=END_YEAR&pi=PROJECT_ID&t=TIME_OF_EXECUTION&u=USERNAME&f=FORMAT&sha1=SHA-1_TO_PROVE_IDENTITY
  
  from pandas.io.json import json_normalize
  r = requests.get(finalquery)
  print(r.text)

  write_a_RH_file(r.text)
#   df = pd.read_json('/tmp/visitors.json')
  with open('/tmp/RH_visitors.json','r') as f:
    data = json.loads(f.read())
# Flatten data
  df_nested_list = pd.json_normalize(data, record_path =['sc_data'])
  print(df_nested_list['date'],df_nested_list['unique_visits'])

  df_nested_list_as_csv = df_nested_list.to_csv(index=False)
#   print(df.head(10))
  
  csv_bytes = bytes(df_nested_list_as_csv, 'utf-8') # fix  
  m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name='RH_visitors.csv')
  
  file_row = app_tables.my_files.get(name='RH_visitors.csv')
  Organisation = app_tables.organisation.get(id = 1)
  client = tz.tzoffset(seconds=offset)
  now = datetime.now(client)
  if file_row != None:
    file_row["media_obj"] = m 
    file_row["last_uploaded"] = now
#       alert('File updated')
  else:
#       alert('File does not exist - adding new file')
    app_tables.my_files.add_row(
    name='RH_visitors.csv', 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now) 
  
@anvil.server.callable 
def write_a_RH_file(my_string):
  #   with open('/tmp/visitors.json', 'w+') as f:
  #     f.write(my_string)
  #   import json
  
    with open('/tmp/RH_visitors.json', 'w+') as f:
      f.write(my_string)
      
@anvil.server.callable  
def SH1Hash(name):
  
  import hashlib
  import xml.etree.ElementTree as ET
  
  myhash = hashlib.sha1(name.encode('utf-8'))
  myhash = myhash.hexdigest()
  myhash =str(myhash)
  return myhash