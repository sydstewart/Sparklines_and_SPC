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

@anvil.server.callable 

def get_usgb(offset, ticker):
    import yfinance as yf
    Organisation = app_tables.organisation.get(id = 1)
    start = datetime(2021,5,31) 
    end =  date.today()   #datetime(2021,6,30) 
    EXCHR = yf.Ticker(ticker) 
#     print(EXCHR.history(start=start, end=end))
    
    df = yf.download(ticker, start="2019-05-31", end=date.today(),group_by="ticker") 
#     print (df) 
#     print (1/df['Open'])
#     df['Open'] = (1/df['Open'])
# #     df.to_csv (r'C:\Users\sydne\Desktop\GBPX.csv', index = False, header=True)
#     print("Open=",df['Open'])
  # set the index
#     print('Columns are',df.columns)
#     print('Index is',df.index)
    
    # reset dataframe index so it shows as a column
    df.reset_index(inplace=True)
#     df.set_index('Date', inplace=False)
#     dt = df.to_dict("record")
#     df['Date']= pd.to_datetime(df['Date'])
#     df.Date.dt.strftime('%Y%m%d').astype(int)
  #   content = io.BytesIO()
  #   df.to_csv(content, index=False)
  #   content.seek(0, 0)
  #   m = anvil.BlobMedia(content=content.read(), content_type="application/vnd.ms-excel", name='nps.csv')
#     df = df[["Date","Open"]]
  #   encoding = 'utf-8' # or alternatively 'ISO-8859-1', etc...
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
  