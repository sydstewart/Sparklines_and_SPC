import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import anvil.secrets

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

NPS_KEY = anvil.secrets.get_secret('customer_thermometer_api+key')



@anvil.server.callable 

def get_nps_responses(offset):
  fromdate = date(2017, 1, 1)
  todate =  fromdate + timedelta(7)
  getMethod ='getNumResponsesValue'
  Organisation = app_tables.organisation.get(id = 1)
  print(Organisation['OrganisationName'])
  df = pd.DataFrame(columns=['Date_entered', 'NPS_reponses'])
  while fromdate <= date.today(): #date(2021, 6, 10):
      
      todate =  fromdate + timedelta(7)
    
    
      url = 'https://app.customerthermometer.com/api.php?'
        
        # defining a params dict for the parameters to be sent to the API
      PARAMS = {'apiKey':NPS_KEY,'getMethod':getMethod,'fromDate':fromdate ,'toDate' :todate }
        
      x = requests.get(url = url, params = PARAMS)
      x = x.content
#       x = x.decode("utf-8")
      x  = int(x) 
      
      df = df.append({'Date_entered': fromdate, 'NPS_responses':x}, ignore_index=True)

          
      fromdate =  todate
  df
  df['Date_entered']= pd.to_datetime(df['Date_entered'])

  df_as_csv = df.to_csv(index=False)
  print(df)
  csv_bytes = bytes(df_as_csv, 'utf-8') # fix  
  
  filename = 'nps_responses.csv'
  
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
    name= filename, 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now )