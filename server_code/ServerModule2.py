import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server
import pandas as pd
import datetime as dt
from datetime import datetime

import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import anvil.secrets
import numpy as np
import matplotlib.pyplot as plt
import anvil.mpl_util
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
import matplotlib.dates as mdates 
from datetime import datetime, timedelta 
 
@anvil.server.callable  
def getsheet():
  
    dfx = pd.DataFrame({'Color': ['Red', 'Yellow', 'Blue', 'Red'], 'Value': [1 , 1 , 1 , 1]})
    print('dfx')
    print(dfx)
    dfx = dfx.groupby(['Color']).size().reset_index(name='cx')
#     dfx['Counts'] = dfx.groupby(['Color'])['Value'].transform('count')
    print(dfx)
    
    
    Organisation = app_tables.organisation.get(id = 1)
    data = app_files.change_notes
    print(data) 

    ws = data["Sheet 1"]
    
    df = pd.DataFrame(columns=['Create_Date', 'Class','Count'])
    
    for r in data["Sheet 1"].rows:
        if r['Class'] == "Defect":
#             print(f"{r['Create_Date']} is {r['Class']} ")
           
            df = df.append({'Create_Date': r['Create_Date'], 'Class': r['Class']}, ignore_index=True)

    print('df')
    
  
    
    df['Create_Date']= pd.to_datetime(df['Create_Date'])
    start_date = "2019-01-01"
    df = df.loc[(df['Create_Date'] >= start_date)]
     
    print(df.head(50))
    df['YM'] = df['Create_Date'].dt.strftime("%Y-%m-01")
#     df['YM'] = pd.to_datetime(df['Create_Date']).dt.strftime('01-%m-%Y')
    print(df['YM'])
    df = df.groupby(df['YM']).size().reset_index(name='cx')
    
    print('groups')
    print(df)

    df['YM']= pd.to_datetime(df['YM'])
    df_as_csv =  df.to_csv(index=False, date_format='%Y/%m/%d')
    
    csv_bytes = bytes(df_as_csv, 'utf-8') # fix  
  
    filename = 'changenote_defects.csv'
  
    m=anvil.BlobMedia('application/vnd.ms-excel', csv_bytes, name=filename)
  
    file_row = app_tables.my_files.get(name=filename)
#     client = tz.tzoffset(seconds=offset)
    now = datetime.now()
  
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
    
    
    years = (df['YM'])
    x = np.arange(len(years))
  
    # Plot it in the normal Matplotlib way
    ax = plt.gca()
    
    
    
    formatter = mdates.DateFormatter("%Y-%m")
     
    
    ax.xaxis.set_major_formatter(formatter)
    
    locator = mdates.DayLocator()
    
    ax.xaxis.set_major_locator(locator)

    plt.figure(1, figsize=(10,5))
    plt.plot(x, df['cx'], 'crimson')  
    
    # Return this plot as a PNG image in a Media object
    return anvil.mpl_util.plot_image()


