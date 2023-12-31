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
  
#     dfx = pd.DataFrame({'Color': ['Red', 'Yellow', 'Blue', 'Red'], 'Value': [1 , 1 , 1 , 1]})
#     print('dfx')
#     print(dfx)
#     dfx = dfx.groupby(['Color']).size().reset_index(name='cx')
# #     dfx['Counts'] = dfx.groupby(['Color'])['Value'].transform('count')
#     print(dfx)
    
    
    Organisation = app_tables.organisation.get(id = 1)
    datachange = app_files.change_notes
    print('dftchange')
    dft  = pd.DataFrame( columns = ['Create_Date', 'Class', 'Year-Month' ])
   
   
    for r in datachange["Sheet 1"].rows:
#        if (r['Create_Date'] == '12/04/2018 10:43'):
#             print(f"{r['Create_Date']} is {r['Class']} ")
            dft = dft.append({'Create_Date': r['Create_Date'], 'Class': r['Class'], 'Year-Month' :r['Year-Month']}, ignore_index=True) 
    print('dft')

    dft = dft.loc[(dft['Class'] == 'Defect')  ]
    dftg = dft.groupby('Year-Month').size().reset_index().rename(columns={0: 'count_changes'})
    print('dftgroup')
    print(dftg)
 
    
  
    
#     df['Create_Date']= pd.to_datetime(df['Create_Date'])
#     start_date = "2019-01-01"
#     df = df.loc[(df['Create_Date'] >= start_date)]
     
#     print(df.head(50))
#     df['YM'] = df['Create_Date'].dt.strftime("%Y-%m-01")
# #     df['YM'] = pd.to_datetime(df['Create_Date']).dt.strftime('01-%m-%Y')
#     print(df['YM'])
#     df = df.groupby(df['YM']).size().reset_index(name='cx')
    
#     print('groups')
#     print(df)

    dftg['YM']= pd.to_datetime(dftg['Year-Month'])
    dftg_as_csv =  dftg.to_csv(index=False, date_format='%Y/%m/%d')
    
    csv_bytes = bytes(dftg_as_csv, 'utf-8') # fix  
  
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
    
    
    years = (dftg['YM'])
    x = np.arange(len(years))
  
    # Plot it in the normal Matplotlib way
    ax = plt.gca()
    
    
    
    formatter = mdates.DateFormatter("%Y-%m")
     
    
    ax.xaxis.set_major_formatter(formatter)
    
    locator = mdates.DayLocator()
    
    ax.xaxis.set_major_locator(locator)

    plt.figure(1, figsize=(10,5))
    plt.plot(x, dftg['count_changes'], 'crimson')  
    
    # Return this plot as a PNG image in a Media object
    return anvil.mpl_util.plot_image()

@anvil.server.callable  
def getsheet_improvements():
  
#     dfx = pd.DataFrame({'Color': ['Red', 'Yellow', 'Blue', 'Red'], 'Value': [1 , 1 , 1 , 1]})
#     print('dfx')
#     print(dfx)
#     dfx = dfx.groupby(['Color']).size().reset_index(name='cx')
# #     dfx['Counts'] = dfx.groupby(['Color'])['Value'].transform('count')
#     print(dfx)
    
    
    Organisation = app_tables.organisation.get(id = 1)
    datachange = app_files.change_notes
    print('dftchange')
    dft  = pd.DataFrame( columns = ['Create_Date', 'Class', 'Year-Month','Stage' ])
   
   
    for r in datachange["Sheet 1"].rows:
#        if (r['Create_Date'] == '12/04/2018 10:43'):
#             print(f"{r['Create_Date']} is {r['Class']} ")
            dft = dft.append({'Create_Date': r['Create_Date'], 'Class': r['Class'], 'Year-Month' :r['Year-Month'], 'Stage' :r['Stage']}, ignore_index=True) 
    print('dft')

    dft = dft.loc[(dft['Class'] == 'Improvement') & (dft['Stage'] == 'Released')  ]
    dftg = dft.groupby('Year-Month').size().reset_index().rename(columns={0: 'count_changes'})
    print('dftgroup')
    print(dftg)
 
    
  
    
#     df['Create_Date']= pd.to_datetime(df['Create_Date'])
#     start_date = "2019-01-01"
#     df = df.loc[(df['Create_Date'] >= start_date)]
     
#     print(df.head(50))
#     df['YM'] = df['Create_Date'].dt.strftime("%Y-%m-01")
# #     df['YM'] = pd.to_datetime(df['Create_Date']).dt.strftime('01-%m-%Y')
#     print(df['YM'])
#     df = df.groupby(df['YM']).size().reset_index(name='cx')
    
#     print('groups')
#     print(df)

    dftg['YM']= pd.to_datetime(dftg['Year-Month'])
    dftg_as_csv =  dftg.to_csv(index=False, date_format='%Y/%m/%d')
    
    csv_bytes = bytes(dftg_as_csv, 'utf-8') # fix  
  
    filename = 'changenote_improvements.csv'
  
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
    
    
    years = (dftg['YM'])
    x = np.arange(len(years))
  
    # Plot it in the normal Matplotlib way
    ax = plt.gca()
    
    
    
    formatter = mdates.DateFormatter("%Y-%m")
     
    
    ax.xaxis.set_major_formatter(formatter)
    
    locator = mdates.DayLocator()
    
    ax.xaxis.set_major_locator(locator)

    plt.figure(1, figsize=(10,5))
    plt.plot(x, dftg['count_changes'], 'crimson')  
    
    # Return this plot as a PNG image in a Media object
    return anvil.mpl_util.plot_image()

  
@anvil.server.callable  
def getsheet_defects_fixed():
  
#     dfx = pd.DataFrame({'Color': ['Red', 'Yellow', 'Blue', 'Red'], 'Value': [1 , 1 , 1 , 1]})
#     print('dfx')
#     print(dfx)
#     dfx = dfx.groupby(['Color']).size().reset_index(name='cx')
# #     dfx['Counts'] = dfx.groupby(['Color'])['Value'].transform('count')
#     print(dfx)
    
    
    Organisation = app_tables.organisation.get(id = 1)
    datachange = app_files.change_notes
    print('dftchange')
    dft  = pd.DataFrame( columns = ['Create_Date', 'Class', 'Year-Month','Stage' ])
   
   
    for r in datachange["Sheet 1"].rows:
#        if (r['Create_Date'] == '12/04/2018 10:43'):
#             print(f"{r['Create_Date']} is {r['Class']} ")
            dft = dft.append({'Create_Date': r['Create_Date'], 'Class': r['Class'], 'Year-Month' :r['Year-Month'], 'Stage' :r['Stage']}, ignore_index=True) 
    print('dft')

    dft = dft.loc[(dft['Class'] == 'Defect') & (dft['Stage'] == 'Released')  ]
    dftg = dft.groupby('Year-Month').size().reset_index().rename(columns={0: 'count_changes'})
    print('dftgroup')
    print(dftg)
 
    
  
    
#     df['Create_Date']= pd.to_datetime(df['Create_Date'])
#     start_date = "2019-01-01"
#     df = df.loc[(df['Create_Date'] >= start_date)]
     
#     print(df.head(50))
#     df['YM'] = df['Create_Date'].dt.strftime("%Y-%m-01")
# #     df['YM'] = pd.to_datetime(df['Create_Date']).dt.strftime('01-%m-%Y')
#     print(df['YM'])
#     df = df.groupby(df['YM']).size().reset_index(name='cx')
    
#     print('groups')
#     print(df)

    dftg['YM']= pd.to_datetime(dftg['Year-Month'])
    dftg_as_csv =  dftg.to_csv(index=False, date_format='%Y/%m/%d')
    
    csv_bytes = bytes(dftg_as_csv, 'utf-8') # fix  
  
    filename = 'defects_released.csv'
  
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
    
    
    years = (dftg['YM'])
    x = np.arange(len(years))
  
    # Plot it in the normal Matplotlib way
    ax = plt.gca()
    
    
    
    formatter = mdates.DateFormatter("%Y-%m")
     
    
    ax.xaxis.set_major_formatter(formatter)
    
    locator = mdates.DayLocator()
    
    ax.xaxis.set_major_locator(locator)

    plt.figure(1, figsize=(10,5))
    plt.plot(x, dftg['count_changes'], 'crimson')  
    
    # Return this plot as a PNG image in a Media object
    return anvil.mpl_util.plot_image()
