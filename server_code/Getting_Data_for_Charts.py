import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

from . import ols_data

  #ALL POINTS 
@anvil.server.callable  
def get_pdcalls(chartid,start_date, end_date):
    import pandas as pd
    import anvil.server
    from tables import app_tables
#     from ServerPackage2.get_dataframe import get_dataframe
    dfcsv, nameCol, dateCol, title, conf_limit, formatCol , noteCol = ols_data(chartid)
    
    scatter = [go.Scatter(x=dfcsv[dateCol],
                              y= dfcsv[nameCol],
    
                            mode='markers+lines',
                              name='All Points',
                              visible = True,
    #                           yaxis ='y0',
    #                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                              line=dict(color='firebrick', width=1)),
      #                          line=dict(color='#2196f3')),
#                   go.Scatter(x=dfcsv[dateCol], y=dfcsv[nameCol], mode='text',
#                         name='Annotations', text=dfcsv[noteCol], textposition='top left')
                  ]
        
    return scatter

@anvil.server.callable  
def get_pdcalls_table(chartid,start_date, end_date):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    from ServerPackage2.get_dataframe import get_dataframe
    dfcsv, nameCol, dateCol, title, conf_limit, formatCol = ols_data(chartid)
    
    scatter = [go.table(x=dfcsv[dateCol],
                              y= dfcsv[nameCol],
    
                            mode='markers+lines',
                              name='All Points',
                              visible = True,
    #                           yaxis ='y0',
    #                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                              line=dict(color='firebrick', width=1)),
      #                          line=dict(color='#2196f3')),
                  ]
        
    return scatter

@anvil.server.callable
def get_dataframe(chart_title):


    
    import pandas as pd
    import anvil.server
    from tables import app_tables
    import datetime as dt
    import io
    
    t = app_tables.charts.get(title=chart_title)
    nameCol = t['nameCol']
    dateCol = t['dateCol']
    title =  t['title']
    fileName =t['fileName']
    id=t['id']
    start_date =t['startDate']
    end_date =t['endDate']
    conf_limit =t['confLimit']
    formal_col=t['formatCol']
    print(fileName)
    mname = app_tables.my_files.get(name=fileName)
    print(mname)
    #     mname =app_tables.my_files.get(name = fileName)['name'] 
    print(start_date)
    if mname != None:
        m=app_tables.my_files.get(name = fileName)['media_obj'] 
    #Convert start and end date to date format to do dataframe filtering
        
          
        print('StartDate=',start_date)
    #         start_date = dt.datetime.strptime(start_date,'%d/%M/%Y')
    #         end_date = dt.datetime.strptime(end_date,'%d/%M/%Y')
        
        dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol], dayfirst=True, infer_datetime_format=True)    
        
    #         print(datetime.now().strftime('%d %B %Y %H:%M') )
        dfcsv[nameCol] = dfcsv[nameCol].astype(float)
        dfcsv['mean'] = dfcsv[nameCol].mean()
        dfcsv['meandiff'] = dfcsv[nameCol] - dfcsv['mean']
        dfcsv['cusum']=dfcsv['meandiff'].cumsum()
        dfcsv=dfcsv.round(3)
        print(datetime.now().strftime('%d %B %Y %H:%M') )
    #         dfcsv[dateCol]= pd.to_datetime(dfcsv[dateCol])
        print(dfcsv[dateCol])
        dfcsv['Mov_avg8'] = dfcsv[nameCol].rolling(window=8).mean()
    #         print(datetime.now().strftime('%d %B %Y %H:%M') )
    #     print(dfcsv)
        # dataframe filtering by date
        dfcsv = dfcsv.loc[(dfcsv[dateCol] >= start_date) & (dfcsv[dateCol] <= end_date)]
    #         dfcsv = dfcsv.loc[(dfcsv[dateCol] >= start_date) & (dfcsv[dateCol] <= end_date)]
#         print(dfcsv)
    return dfcsv, nameCol, dateCol,format_col