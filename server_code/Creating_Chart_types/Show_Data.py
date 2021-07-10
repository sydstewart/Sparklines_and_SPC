import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io
import plotly.graph_objects as go

@anvil.server.callable  
def showdata(chartid,  filename):
     t = app_tables.charts.get(id=chartid)
     filename =t['file_name']['name']
     m=app_tables.my_files.get(name = filename)['media_obj'] 
     dateCol = t['dateCol']
     nameCol = t['nameCol']
     dayfirst = t['DateDayFirst']
     dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates= [dateCol] , dayfirst=dayfirst, infer_datetime_format=True)
     dfcsv[dateCol] =  pd.to_datetime(dfcsv[dateCol]).dt.strftime('%Y/%m/%d')
     dfcsv[nameCol] = dfcsv[nameCol] .map(lambda x: '{0:,.2f}'.format(x))
#      cols = [dateCol,nameCol]
#      dfcsv = dfcsv[dfcsv.columns[cols]]
#      dfcsv[nameCol] = dfcsv[nameCol].round(2)
#      dfcsv[dateCol]   = pd.to_datetime(dfcsv[dateCol])
     # Format with commas and round off to two decimal places in pandas
#      pd.options.display.float_format = "{:,.2f}".format
     dfcsv = dfcsv.sort_values(by=dfcsv.columns[0], ascending=False)
#      columnlist = [dateCol,nameCol]
     data=[go.Table(
          header=dict(values= [dateCol,nameCol], # values=list(df.columns)
                      line_color='darkslategray',
                      fill_color='lightskyblue',
                      align='center'),
          cells=dict(values=[(dfcsv[dateCol]),dfcsv[nameCol]], # 2nd column
                    line_color='darkslategray',
                    fill_color='lightcyan',
                    align='center'))
      ]
     return data
