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
import plotly.graph_objects as go
from .control_charts import ols_data
from datetime import date, datetime
import io
import plotly


@anvil.server.callable
def add_stacked_chart(new_stacked_chart):
  max_value = app_tables.charts.search(tables.order_by("id", ascending=False))[0]['id']
  max_value = max_value + 1     
  current_user = anvil.users.get_user()
  
  app_tables.charts.add_row(**new_stacked_chart,id = max_value,updated_last = datetime.now(), archive = False,End_date_Overwrite = False, )
#   app_tables.folder_shares.add_row( id = max_value,updated_last = datetime.now(),FolderUser=current_user)






@anvil.server.callable
def get_stacked_Improvements():
  
 
    
    chartid1 = 72
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = ols_data(chartid1)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
    d1 = today.strftime("%Y-%m-01")
    dfcsv1['YM'] = dfcsv1[dateCol1]
    dfcsv1["YM"] = pd.to_datetime(dfcsv1["YM"])
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv1['YM'].min(),end=d1,freq="MS")})
    
    dfcsv1 = pd.merge(all_dates, dfcsv1, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv1['nameColcusum1'] = dfcsv1[nameCol1] 
    dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
    
    chartid2 = 73
    dfcsv2, nameCol2, dateCol2, title2, conf_limit2, formatCol2 = ols_data(chartid2)
    dfcsv2['YM'] = dfcsv2[dateCol2]
    dfcsv2["YM"] = pd.to_datetime(dfcsv2["YM"])
    
    dfcsv2 = pd.merge(all_dates, dfcsv2, how="left", on='YM').fillna(0)
    
    dfcsv2['nameColcusum2'] = dfcsv2[nameCol2] 
    dfcsv2['nameColcusum2'] = dfcsv2['nameColcusum2'].cumsum()
    
    chartid3 = 74
    dfcsv3, nameCol3, dateCol3, title3, conf_limit3, formatCol3 = ols_data(chartid3)
    dfcsv3['YM'] = dfcsv3[dateCol3]
    dfcsv3["YM"] = pd.to_datetime(dfcsv3["YM"])
    
    dfcsv3 = pd.merge(all_dates, dfcsv3, how="left", on='YM').fillna(0)
   
    dfcsv3['nameColcusum3'] = dfcsv3[nameCol3] 
    dfcsv3['nameColcusum3'] = dfcsv3['nameColcusum3'].cumsum()
    
    chartid4 = 75
    dfcsv4, nameCol4, dateCol4, title4, conf_limit4, formatCol4 = ols_data(chartid4)
    dfcsv4['YM'] = dfcsv4[dateCol4]
    dfcsv4["YM"] = pd.to_datetime(dfcsv4["YM"])
    
    dfcsv4 = pd.merge(all_dates, dfcsv4, how="left", on='YM').fillna(0)
   
    dfcsv4['nameColcusum4'] = dfcsv4[nameCol4] 
    dfcsv4['nameColcusum4'] = dfcsv4['nameColcusum4'].cumsum()
 
    
    chartid5 = 76
    dfcsv5, nameCol5, dateCol5, title5, conf_limit5, formatCol5 = ols_data(chartid5)
    dfcsv5['YM'] = dfcsv5[dateCol5]
    dfcsv5["YM"] = pd.to_datetime(dfcsv5["YM"])
    
    dfcsv5= pd.merge(all_dates, dfcsv5, how="left", on='YM').fillna(0)
   
    dfcsv5['nameColcusum5'] = dfcsv5[nameCol5] 
    dfcsv5['nameColcusum5'] = dfcsv5['nameColcusum5'].cumsum()
    
    chartid6 = 85
    dfcsv6, nameCol6, dateCol6, title6, conf_limit6, formatCol6 = ols_data(chartid6)
    dfcsv6['YM'] = dfcsv6[dateCol6]
    dfcsv6["YM"] = pd.to_datetime(dfcsv6["YM"])
    
    dfcsv6= pd.merge(all_dates, dfcsv6, how="left", on='YM').fillna(0)
   
    dfcsv6['nameColcusum6'] = dfcsv6[nameCol6] 
    dfcsv6['nameColcusum6'] = dfcsv6['nameColcusum6'].cumsum()
    
    chartid7 = 89
    dfcsv7, nameCol7, dateCol7, title7, conf_limit7, formatCol7 = ols_data(chartid7)
    dfcsv7['YM'] = dfcsv7[dateCol7]
    dfcsv7["YM"] = pd.to_datetime(dfcsv7["YM"])
    
    dfcsv7= pd.merge(all_dates, dfcsv7, how="left", on='YM').fillna(0)
   
    dfcsv7['nameColcusum7'] = dfcsv7[nameCol7] 
    dfcsv7['nameColcusum7'] = dfcsv7['nameColcusum7'].cumsum()
    
    fig = go.Figure()
    

    fig.add_trace(go.Scatter(
        x=dfcsv1[dateCol1],y= dfcsv1['nameColcusum1'],
        hoverinfo='x+y',
        mode='lines',
        name='Defect Change Notes',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=dfcsv3[dateCol3],y= dfcsv3['nameColcusum3'],
        hoverinfo='x+y',
        mode='lines',
        name='RCA actions completed',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=dfcsv2[dateCol2],y= dfcsv2['nameColcusum2'],
        hoverinfo='x+y',
        mode='lines',
        name='Improvement Change Notes',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=dfcsv1[dateCol1],y= dfcsv4['nameColcusum4'],
        hoverinfo='x+y',
        mode='lines',
        name='Implementation Lessons Learnt',
        line=dict(width=0.5, color='blue'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=dfcsv6[dateCol6],y= dfcsv6['nameColcusum6'],
        hoverinfo='x+y',
        mode='lines',
        name='Audit NC Improvement Actions',
        line=dict(width=0.5, color='brown'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=dfcsv5[dateCol5],y= dfcsv5['nameColcusum5'],
        hoverinfo='x+y',
        mode='lines',
        name='Documentation/Methods Improvements',
        line=dict(width=0.5, color='green'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=dfcsv5[dateCol7],y= dfcsv7['nameColcusum7'],
        hoverinfo='x+y',
        mode='lines',
        name='Infrastructure Improvements',
        line=dict(width=0.5, color='purple'),
        stackgroup='one'
    ))

    # Change grid color and axis colors
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black') #, gridcolor='black')
    fig.update_yaxes(showline=True, linewidth=1)  #, linecolor='gray')
    fig.update_xaxes(tickangle= 45)
    fig.update_layout(plot_bgcolor='rgb(235, 240, 237)')
    fig.update_layout(height=1600, width=800, title_text='Improvement Actions')
#     img_bytes = fig.to_image(format="png", width=600, height=350, scale=2)
#     plotly.io.orca.write_image(fig, '/tmp/fig1.jpg', format='jpg') #, scale=None, width=None, height=None, validate=True, engine='auto')
    return fig

    
@anvil.server.callable
def get_stacked_RCA():
  
 
    
    chartid1 = 83
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = ols_data(chartid1)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
    d1 = today.strftime("%Y-%m-01")
    dfcsv1['YM'] = dfcsv1[dateCol1]
    dfcsv1["YM"] = pd.to_datetime(dfcsv1["YM"])
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv1['YM'].min(),end=d1,freq="MS")})
    
    dfcsv1 = pd.merge(all_dates, dfcsv1, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv1['nameColcusum1'] = dfcsv1[nameCol1] 
    dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
    
    chartid2 = 82
    dfcsv2, nameCol2, dateCol2, title2, conf_limit2, formatCol2 = ols_data(chartid2)
    dfcsv2['YM'] = dfcsv2[dateCol2]
    dfcsv2["YM"] = pd.to_datetime(dfcsv2["YM"])
    
    dfcsv2 = pd.merge(all_dates, dfcsv2, how="left", on='YM').fillna(0)
    
    dfcsv2['nameColcusum2'] = dfcsv2[nameCol2] 
    dfcsv2['nameColcusum2'] = dfcsv2['nameColcusum2'].cumsum()
    
#     chartid3 = 74
#     dfcsv3, nameCol3, dateCol3, title3, conf_limit3, formatCol3 = ols_data(chartid3)
#     dfcsv3['YM'] = dfcsv3[dateCol3]
#     dfcsv3["YM"] = pd.to_datetime(dfcsv3["YM"])
    
#     dfcsv3 = pd.merge(all_dates, dfcsv3, how="left", on='YM').fillna(0)
   
#     dfcsv3['nameColcusum3'] = dfcsv3[nameCol3] 
#     dfcsv3['nameColcusum3'] = dfcsv3['nameColcusum3'].cumsum()
    
#     chartid4 = 75
#     dfcsv4, nameCol4, dateCol4, title4, conf_limit4, formatCol4 = ols_data(chartid4)
#     dfcsv4['YM'] = dfcsv4[dateCol4]
#     dfcsv4["YM"] = pd.to_datetime(dfcsv4["YM"])
    
#     dfcsv4 = pd.merge(all_dates, dfcsv4, how="left", on='YM').fillna(0)
   
#     dfcsv4['nameColcusum4'] = dfcsv4[nameCol4] 
#     dfcsv4['nameColcusum4'] = dfcsv4['nameColcusum4'].cumsum()
 
    
#     chartid5 = 76
#     dfcsv5, nameCol5, dateCol5, title5, conf_limit5, formatCol5 = ols_data(chartid5)
#     dfcsv5['YM'] = dfcsv5[dateCol5]
#     dfcsv5["YM"] = pd.to_datetime(dfcsv5["YM"])
    
#     dfcsv5= pd.merge(all_dates, dfcsv5, how="left", on='YM').fillna(0)
   
#     dfcsv5['nameColcusum5'] = dfcsv5[nameCol5] 
#     dfcsv5['nameColcusum5'] = dfcsv5['nameColcusum5'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dfcsv1[dateCol1],y= dfcsv1['nameColcusum1'],
        hoverinfo='x+y',
        mode='lines',
        name='RCAs Completed',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=dfcsv2[dateCol2],y= dfcsv2['nameColcusum2'],
        hoverinfo='x+y',
        mode='lines',
        name='RCAs In Progress',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
#     fig.add_trace(go.Scatter(
#         x=dfcsv3[dateCol3],y= dfcsv3['nameColcusum3'],
#         hoverinfo='x+y',
#         mode='lines',
#         name='RCA actions completed',
#         line=dict(width=0.5, color='rgb(184, 247, 212)'),
#         stackgroup='one'
#     ))
#     fig.add_trace(go.Scatter(
#         x=dfcsv1[dateCol1],y= dfcsv4['nameColcusum4'],
#         hoverinfo='x+y',
#         mode='lines',
#         name='Implementation Lessons Learnt',
#         line=dict(width=0.5, color='blue'),
#         stackgroup='one'
#     ))
#     fig.add_trace(go.Scatter(
#         x=dfcsv5[dateCol5],y= dfcsv5['nameColcusum5'],
#         hoverinfo='x+y',
#         mode='lines',
#         name='Documentation/Methods Improvements',
#         line=dict(width=0.5, color='green'),
#         stackgroup='one'
#     ))
    # Change grid color and axis colors
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black') #, gridcolor='black')
    fig.update_yaxes(showline=True, linewidth=1)  #, linecolor='gray')
    fig.update_xaxes(tickangle= 45)
    fig.update_layout(plot_bgcolor='rgb(235, 240, 237)')
    fig.update_layout(height=1600, width=800, title_text='RCAs')
    return fig    