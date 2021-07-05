import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import pandas as pd
import io

@anvil.server.callable
def chart_columns(fileName):
  
    m=app_tables.my_files.get(name = fileName['name'])['media_obj'] 
#     t= app_tables.charts.get(file_name=fileName)
#     chartid = t['id']
#     dayfirst = t['DateDayFirst']
  #         print('DayFirst', dayfirst)
  #         dayfirst is FALSE for DD/MM  = MM/DD True
    #Read in data file csv
    dfcsv=pd.read_csv(io.BytesIO(m.get_bytes())) # ,parse_dates=[dateCol] , dayfirst= True, infer_datetime_format=True)
#     dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol])
    columns = list(dfcsv.columns) 
    print(columns)
    for i in columns:
        print(i)
    return columns
  
@anvil.server.callable
def search_columns(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False