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


from datetime import datetime, timedelta, timezone
from anvil import tz

# @anvil.server.callable
# def what_time(offset):
#   client = tz.tzoffset(seconds=offset)
#   now = datetime.now(client)
#   print('currenttime',now)

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.email.handle_message
def handle_incoming_emails(msg):

  msg.reply(text="Thank you for your message OK .")
  print(msg)
  hoursoffset = 1
  msg_row = app_tables.received_messages.add_row(
              from_addr=msg.envelope.from_address, 
              to=msg.envelope.recipient,
              text=msg.text, 
              html=msg.html,
              received_time = datetime.now()
              
            )
  Organisation = app_tables.organisation.get(id = 1)
  print(Organisation['OrganisationName'])
  for a in msg.attachments:
    
    file_row = app_tables.my_files.get(name=msg.html)
    if file_row != None:
      file_row["media_obj"] = a
      file_row["last_uploaded"] = datetime.now() + timedelta(hours=hoursoffset)
#       alert('File updated')
    else:
#       alert('File does not exist - adding new file')
      app_tables.my_files.add_row(
      name=msg.html, 
      media_obj=a,
      Organisation = Organisation,
      last_uploaded = datetime.now() + timedelta(hours=hoursoffset))
      
      file_row = app_tables.my_files.get(name=msg.html)
      
      if file_row != None:
          alert('File added')
      else:
          alert('File not added successfully')
    
  
@anvil.server.callable
def send_email(address):
    with open('/tmp/fig1.html', 'r') as f:
      contents = f.read()
      print(contents)
    anvil.email.send(
      from_name="Syd Stewart",
      to=address,
      subject="Improvements",   
#       html="<h1>Welcome!</h1>",
      html=""" Here's a picture:<br> <img src="cid:mypic"><br> Wasn't that cute? """,
      inline_attachments={'mypic': picture}
#       text="The Anvil Forum (https://anvil.works/forum) is friendly and informative.",
#       attachments= /tmp/fig1.html
    )


NPS_KEY = anvil.secrets.get_secret('customer_thermometer_api+key')

@anvil.server.callable 

def get_nps(offset):
  fromdate = date(2017, 1, 1)
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
  
@anvil.server.callable
def make_data(**kwargs):
  x_arr = np.array([[1,2,3]]) #placeholder data
  X = pd.DataFrame(x_arr)
  X.to_csv('/tmp/X.csv')
  X_media = anvil.media.from_file('/tmp/X.csv', 'csv', 'X')
  return X_media
 
@anvil.server.callable  
def tables(chartid, filename):
     t = app_tables.charts.get(id=chartid)
     filename =t['file_name']['name']
     m=app_tables.my_files.get(name = filename)['media_obj'] 
     dateCol = t['dateCol']
     nameCol = t['nameCol']
     dayfirst = t['DateDayFirst']
     dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol] , dayfirst=dayfirst, infer_datetime_format=True)
     dfcsv[dateCol] =  pd.to_datetime(dfcsv[dateCol]).dt.strftime('%Y/%m/%d')
     dfcsv[nameCol] = dfcsv[nameCol] .map(lambda x: '{0:,.2f}'.format(x))
#      dfcsv[nameCol] = dfcsv[nameCol].round(2)
#      dfcsv[dateCol]   = pd.to_datetime(dfcsv[dateCol])
     # Format with commas and round off to two decimal places in pandas
#      pd.options.display.float_format = "{:,.2f}".format
     dfcsv = dfcsv.sort_values(by=dfcsv.columns[0], ascending=False)
     data=[go.Table(
          header=dict(values=list(dfcsv.columns), # values=list(df.columns)
                      line_color='darkslategray',
                      fill_color='lightskyblue',
                      align='right'),
          cells=dict(values=[(dfcsv[dateCol]),dfcsv[nameCol]], # 2nd column
                    line_color='darkslategray',
                    fill_color='lightcyan',
                    align='right'))
      ]
     return data

     

@anvil.server.callable  
def SH1Hash(name):
  
  import hashlib
  import xml.etree.ElementTree as ET
  
  myhash = hashlib.sha1(name.encode('utf-8'))
  myhash = myhash.hexdigest()
  myhash =str(myhash)
  return myhash
  
@anvil.server.callable 
def write_a_file(my_string):
#   with open('/tmp/visitors.json', 'w+') as f:
#     f.write(my_string)
#   import json
 
  with open('/tmp/visitors.json', 'w+') as f:
    f.write(my_string)
    
@anvil.server.callable  
def get_DAS28_statcounter():
  from datetime import timezone
  import xml.etree.ElementTree as ET
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
  projectid = '&pi=7091431'
#   projectid = '&pi=2292634'
  numberofresults ='&n=5'
  timeofquery = '&t='+ str(int(timestamp))
  username = '&u=sydstewart' 
#   username = '&u=demo_user'
  apipassword  = 'Arnside2021'
#   apipassword  = 'statcounter'
  startyear = '&g=daily&sd=01&sm=01&sy=20190&ed=31&em=12&ey=2023'
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
 