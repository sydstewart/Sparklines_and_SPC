import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

# from ..Getting_Data_for_Charts import ols_data


  #ALL POINTS 
@anvil.server.callable  
def get_pdcalls(chartid,start_date, end_date):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    from ServerPackage2.get_dataframe import get_dataframe
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