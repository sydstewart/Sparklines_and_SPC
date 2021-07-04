import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import pandas as pd
from datetime import datetime
import io

@anvil.server.callable
def get_folders():
  #    foldername = app_tables.folders.search(folder_name =folder)
#    loggedin_user = anvil.users.get_user()
#    organisation = loggedin_user['Organisation'] 
   Organisation = app_tables.organisation.get(id = 1)
   user = app_tables.users.get(email= 'sydney.w.stewart@gmail.com')
#    print('0) '+str(datetime.now()))
   rows = app_tables.folder_shares.search(Organisation = Organisation,FolderUser=user)
#    dfs = pd.DataFrame([rows])
   newlist=[]
   for row in rows:
     print(row['Folder']['folder_name'])
     newlist.append(row['Folder']['folder_name'])
   print(newlist)
#    print('1) '+str(datetime.now()))
# tables.order_by("folder_name", ascending = True)
   return rows, newlist

@anvil.server.callable
def get_charts(folderselected):
#    foldername = app_tables.folders.search(folder_name = folderselected)
#    loggedin_user = anvil.users.get_user()
#    organisation = loggedin_user['Organisation'] 
#    Organisation = app_tables.organisation.get(id = 1)
#    user = app_tables.users.get(email= 'sydney.w.stewart@gmail.com')
# #    print('0) '+str(datetime.now()))
   print ('folderselected =',folderselected)
   folder_shares_id = folderselected['id']
   print ('folder_shares_id', folder_shares_id)
   folder_name = folderselected['Folder']['folder_name']
   print('folder_name', folder_name)
#    folderselect = app_tables.folders.search(folder_name=folderselected['folder_name'])
   folder = app_tables.folders.search(folder_name =folderselected['Folder']['folder_name'])
   foldername = folder['folder_name']
   print ('folder name from folders', foldername)
   chart_rows = app_tables.charts.search(folder_name=folder['folder_name']['folder_name'])
#    dfs = pd.DataFrame([rows])
#    newlist=[]
#    for row in rows:
#      print(row['Folder']['folder_name'])
#      newlist.append(row['Folder']['folder_name'])
#    print(newlist)
#    print('1) '+str(datetime.now()))
# tables.order_by("folder_name", ascending = True)
   return chart_rows

@anvil.server.callable
def get_charts_simple(folderselected):
    
#     folder_row = app_tables.folders.get(folder_name = folderselected[fol])
    chart_rows = app_tables.charts.search(folder_name=folderselected)
    return chart_rows
  

@anvil.server.callable
def get_charts_simple_text(text):
    print('text=',text)
    text ='%' + text +'%'
#     folder_row = app_tables.folders.get(folder_name = folderselected[fol])
    chart_rows = app_tables.charts.search(title=q.ilike(text)) 
    return chart_rows



      
@anvil.server.callable
def csv_data(fileName):
  
    m=app_tables.my_files.get(name = fileName)['media_obj'] 
    t= app_tables.charts.get(file_name=fileName)
    chartid = t['id']
    dayfirst = t['DateDayFirst']
  #         print('DayFirst', dayfirst)
  #         dayfirst is FALSE for DD/MM  = MM/DD True
    #Read in data file csv
    dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol] , dayfirst= True, infer_datetime_format=True)
    dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol])
#       print(fileName)
# #       t= app_tables.charts.get(file_name=fileName)
# #       chartid = t['id']
# #       print(chartid)
# #       m=app_tables.my_files.get(name = fileName)
# #       file_Name =m['name']
# #       print('file_anme',file_Name)
# #       t= app_tables.charts.get(file_name=file_Name)
# #       dayfirst = t['DateDayFirst']
# #       print('DayFirst', dayfirst)
# #       file_Name = t['file_name']['name']
# #       mname = app_tables.my_files.get(name=file_Name)
# #       print(mname)
# #     mname =app_tables.my_files.get(name = fileName)['name'] 
# #     print("Start Date=",start_date)
# #     print("End Date=",end_date)
    
# #       if mname != None:
#       m=app_tables.my_files.get(name = fileName)['media_obj'] 
# #       t= app_tables.charts.get(file_name=fileName)
#       dayfirst = True
#       dateCol = 'Date_entered'
#       print('DayFirst', dayfirst)
# #         dayfirst is FALSE for DD/MM  = MM/DD True
#       #Read in data file csv
#       dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()), dayfirst=True, infer_datetime_format=True)
#       dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol])
#       print(dfcsv)
    return dfcsv