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
from .hash import SH1Hash
from .DAS28_statcounter import write_a_file


@anvil.server.callable
# @anvil.server.background_task
def get_api_call():
    """Launch a single crawler background task."""
    
    task = anvil.server.launch_background_task('get_nps_background')
    print("calling chart background generation")
    return task

 
@anvil.server.background_task
def get_nps_background():
    """Launch a single crawler background task."""
    client = tz.tzlocal()
    
    offset = datetime.now(client).utcoffset().seconds
    task = anvil.server.launch_background_task('get_nps_data')
    print("calling chart background generation")
    return task
  

  
@anvil.server.background_task
def get_nps_data():
  client = tz.tzlocal()
    
  offset = datetime.now(client).utcoffset().seconds 
  NPS_KEY = anvil.secrets.get_secret('customer_thermometer_api+key')
  fromdate = date(2018, 1, 8)
  todate =  fromdate + timedelta(7)
  getMethod ='getNPSValue'
  Organisation = app_tables.organisation.get(id = 1)
  print(Organisation['OrganisationName'])
  df = pd.DataFrame(columns=['Date_entered', 'NPS'])
  while fromdate <= date.today(): #date(2021, 6, 10):
      
      todate =  fromdate + timedelta(7)
    
    
      url = 'https://app.customerthermometer.com/api.php?'
        
        # defining a params dict for the parameters to be sent to the API
      PARAMS = {'apiKey':NPS_KEY,'getMethod':getMethod,'fromDate':fromdate ,'toDate' :todate }
        
      x = requests.get(url = url, params = PARAMS)
      x = x.content
#       x = x.decode("utf-8")
      x  = int(x) 
      
      df = df.append({'Date_entered': fromdate, 'NPS':x}, ignore_index=True)

          
      fromdate =  todate
  df
  df['Date_entered']= pd.to_datetime(df['Date_entered'])
#   content = io.BytesIO()
#   df.to_csv(content, index=False)
#   content.seek(0, 0)
#   m = anvil.BlobMedia(content=content.read(), content_type="application/vnd.ms-excel", name='nps.csv')
 
#   encoding = 'utf-8' # or alternatively 'ISO-8859-1', etc...
  df_as_csv = df.to_csv(index=False)
  print(df)
  csv_bytes = bytes(df_as_csv, 'utf-8') # fix  
  m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name='nps.csv')
  


  file_row = app_tables.my_files.get(name='nps.csv')
  client = tz.tzoffset(seconds=offset)
  now = datetime.now(client)
  
  if file_row != None:
    file_row["media_obj"] = m 
    file_row["last_uploaded"] = now
#       alert('File updated')
  else:
#       alert('File does not exist - adding new file')
    app_tables.my_files.add_row(
    name='nps.csv', 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now )

@anvil.server.background_task
def get_nps_background_responses():
    """Launch a single crawler background task."""
    task = anvil.server.launch_background_task('get_nps_responses_background')
    print("calling chart background generation")
    return task  
  
  
  
  
@anvil.server.background_task  
def get_nps_responses_background():
      fromdate = date(2019, 7, 8)
      todate =  fromdate + timedelta(7)
      client = tz.tzlocal()
      offset = datetime.now(client).utcoffset().seconds 
      NPS_KEY = anvil.secrets.get_secret('customer_thermometer_api+key')
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
      
@anvil.server.background_task
def get_AC_background_responses():
    """Launch a single crawler background task."""
    task = anvil.server.launch_background_task('get_AC_statcounter')
    print("calling chart background generation")
    return task        

      
      
      
      
      
@anvil.server.background_task
def get_AC_statcounter():
  from datetime import timezone
  import xml.etree.ElementTree as ET
  from .AC_statcounter import SH1Hash
  client = tz.tzlocal()
  offset = datetime.now(client).utcoffset().seconds 
  
  
  print('offset in AC',offset)
  dt = datetime.now()
  timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
  print(int(timestamp))
  query = 'http://api.statcounter.com/stats/'
  version = '?vn=3'
  visitor = '&s=summary'
  formats = '&f=json'
  projectid = '&pi=3364570'
#   projectid = '&pi=2292634'
  numberofresults ='&n=5'
  timeofquery = '&t='+ str(int(timestamp))
  username = '&u=sydstewart' 
#   username = '&u=demo_user'
  apipassword  = 'Arnside2021'
#   apipassword  = 'statcounter'
  startyear = '&g=daily&sd=01&sm=5&sy=20210&ed=31&em=12&ey=2021'
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

  write_a_AC_file(r.text)
#   df = pd.read_json('/tmp/visitors.json')
  with open('/tmp/AC_visitors.json','r') as f:
    data = json.loads(f.read())
# Flatten data
  df_nested_list = pd.json_normalize(data, record_path =['sc_data'])
  print(df_nested_list['date'],df_nested_list['unique_visits'])

  df_nested_list_as_csv = df_nested_list.to_csv(index=False)
#   print(df.head(10))
  
  csv_bytes = bytes(df_nested_list_as_csv, 'utf-8') # fix  
  m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name='AC_visitors.csv')
  
  file_row = app_tables.my_files.get(name='AC_visitors.csv')
  Organisation = app_tables.organisation.get(id = 1)
  client = tz.tzoffset(seconds=offset)
  now = datetime.now(client)
#   from . import time_stamps
#   now = anvil.server.call('what_time')
#   print('now from AC',now)
  if file_row != None:
    file_row["media_obj"] = m 
    file_row["last_uploaded"] = now
#       alert('File updated')
  else:
#       alert('File does not exist - adding new file')
    app_tables.my_files.add_row(
    name='AC_visitors.csv', 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now) 
  
@anvil.server.callable 
def write_a_AC_file(my_string):
  #   with open('/tmp/visitors.json', 'w+') as f:
  #     f.write(my_string)
  #   import json
  
    with open('/tmp/AC_visitors.json', 'w+') as f:
      f.write(my_string)

@anvil.server.background_task
def get_DAS28_background_responses():
    """Launch a single crawler background task."""
    task = anvil.server.launch_background_task('get_DAS28_statcounter')
    print("calling chart background generation")
    return task        

@anvil.server.background_task
def get_DAS28_statcounter():
  from datetime import timezone
  import xml.etree.ElementTree as ET
  client = tz.tzlocal()
  offset = datetime.now(client).utcoffset().seconds 
   
  print('offset in AC',offset)
  dt = datetime.now()
  timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
  query = 'http://api.statcounter.com/stats/'
  version = '?vn=3'
  visitor = '&s=summary'
  formats = '&f=json'
  projectid = '&pi=7091431'
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

  write_a_file(r.text)
#   df = pd.read_json('/tmp/visitors.json')
  with open('/tmp/visitors.json','r') as f:
    data = json.loads(f.read())
# Flatten data
  df_nested_list = pd.json_normalize(data, record_path =['sc_data'])
  print(df_nested_list['date'],df_nested_list['unique_visits'])

  df_nested_list_as_csv = df_nested_list.to_csv(index=False)
#   print(df.head(10))
  
  csv_bytes = bytes(df_nested_list_as_csv, 'utf-8') # fix  
  m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name='visitors.csv')
  
  file_row = app_tables.my_files.get(name='visitors.csv')
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
    name='visitors.csv', 
    media_obj=m, 
    Organisation = Organisation,
    last_uploaded = now) 
  
  
@anvil.server.background_task
def get_gb_usd_background():
    """Launch a single crawler background task."""
    client = tz.tzlocal()
    ticker = 'GBPUSD=X'
    offset = datetime.now(client).utcoffset().seconds
    task = anvil.server.launch_background_task('get_gb_usd',offset, ticker)
    print("calling chart background generation")
    return task  
  
@anvil.server.background_task
def get_gb_eur_background():
    """Launch a single crawler background task."""
    client = tz.tzlocal()
    ticker = 'GBPEUR=X'
    offset = datetime.now(client).utcoffset().seconds
    task = anvil.server.launch_background_task('get_gb_usd',offset, ticker)
    print("calling chart background generation")
    return task    

@anvil.server.background_task
def get_gb_cad_background():
    """Launch a single crawler background task."""
    client = tz.tzlocal()
    ticker = 'GBPCAD=X'
    offset = datetime.now(client).utcoffset().seconds
    task = anvil.server.launch_background_task('get_gb_usd',offset, ticker)
    print("calling chart background generation")
    return task 
  
@anvil.server.background_task
def get_gb_usd(offset, ticker):
    from . import Globals
#     EXCHR ="GBPUSD=X"
    import yfinance as yf
    Organisation = app_tables.organisation.get(id = 1)
    start = datetime(2021,5,31) 
    end =  date.today()   #datetime(2021,6,30) 
    EXCHR = yf.Ticker(ticker) 
#     print(EXCHR.history(start=start, end=end))
#     ticker = EXCHR
    
    df = yf.download(ticker, start="2019-05-31", end=date.today(),group_by="ticker") 
#     print (df) 

  # set the index
#     print('Columns are',df.columns)
#     print('Index is',df.index)
    
    # reset dataframe index so it shows as a column
    df.reset_index(inplace=True)

    df_as_csv = df.to_csv(index=False)
#     print(df)
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

    
@anvil.server.background_task
def get_data_background():
    """Launch a single crawler background task."""
    client = tz.tzlocal()
    offset = datetime.now(client).utcoffset().seconds
    task = anvil.server.launch_background_task('get_data',offset)
    print("calling chart background generation")
    return task 
  
@anvil.server.background_task
def get_data(offset):
    from . import Globals
    client = tz.tzlocal()
    print('client in AC', client)
    Globals.offset = datetime.now(client).utcoffset().seconds
    items = anvil.server.call('get_items')
    anvil.server.call('convert_dict',items, Globals.offset)
    
    