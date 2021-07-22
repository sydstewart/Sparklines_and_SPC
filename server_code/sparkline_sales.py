import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import plotly.graph_objects as go
from .control_charts import ols_data
import pandas as pd
from datetime import date ,datetime, timedelta
from plotly.subplots import make_subplots
import plotly.io as pio
from anvil import BlobMedia

@anvil.server.callable
def get_sparklines_sales():
    end_date_of_last_month = datetime.today().replace(day=1) - timedelta(1)
    end_date_of_last_month = end_date_of_last_month.strftime("%Y-%m-%d")
    print(end_date_of_last_month)
    
# ===============================================================================     #quotes row 1
    #quotes row 1
    chartid1 = 88
    row1 =1
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1, noteCol1 = ols_data(chartid1)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d1 = today.strftime("%Y-%m-01")

    dfcsv1['YM'] = dfcsv1[dateCol1]
    dfcsv1["YM"] = pd.to_datetime(dfcsv1["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv1['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv1 = pd.merge(all_dates, dfcsv1, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv1['nameColcusum1'] = dfcsv1[nameCol1] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv1['Mean']= dfcsv1['nameColcusum1'].mean()
    
#=====================================================================  New and Exosting Sales row2   

  # New and Exosting Sales row2
    chartid2 = 50
    row2 = 2
    
    dfcsv2, nameCol2, dateCol2, title2, conf_limit2, formatCol2, noteCol2  = ols_data(chartid2)
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv2['YM'].min(),end=end_date_of_last_month,freq="MS")})
    dfcsv2['YM'] = dfcsv2[dateCol2]
    dfcsv2["YM"] = pd.to_datetime(dfcsv2["YM"])
    
    dfcsv2 = pd.merge(all_dates, dfcsv2, how="left", on='YM').fillna(0)
    
    dfcsv2['nameColcusum2'] = dfcsv2[nameCol2]
    
    # calculate mean
    dfcsv2['Mean']= dfcsv2['nameColcusum2'].mean()

#============================================================================================ Total Maint row 3    
    
   #Total Maint row 3 
    chartid3 = 96
    row3 = 3
    
    dfcsv3, nameCol3, dateCol3, title3, conf_limit3, formatCol3, noteCol3  = ols_data(chartid3)
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv3['YM'].min(),end=end_date_of_last_month,freq="MS")})
    dfcsv3['YM'] = dfcsv3[dateCol3]
    dfcsv3["YM"] = pd.to_datetime(dfcsv3["YM"])
    
    dfcsv3 = pd.merge(all_dates, dfcsv3, how="left", on='YM').fillna(0)
    
    dfcsv3['nameColcusum3'] = dfcsv3[nameCol3]
    
    # calculate mean
    dfcsv3['Mean']= dfcsv3['nameColcusum3'].mean()
    
#============================================================================================  #AC Maint  row 4  
    
#AC Maint
        #AC Maint  row 4
    chartid4 = 81
    row4 =4
    dfcsv4, nameCol4, dateCol4, title4, conf_limit4, formatCol4, noteCol4 = ols_data(chartid4)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d4 = today.strftime("%Y-%m-01")

    dfcsv4['YM'] = dfcsv4[dateCol4]
    dfcsv4["YM"] = pd.to_datetime(dfcsv4["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv4['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv4 = pd.merge(all_dates, dfcsv4, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv4['nameColcusum4'] = dfcsv4[nameCol4] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv4['Mean']= dfcsv4['nameColcusum4'].mean()
    
#=====================================================================   #SM Maintenence 
    #SM Maintenence
        #AC Maint  row 5
    chartid5 = 61
    row5 =5
    dfcsv5, nameCol5, dateCol5, title5, conf_limit5, formatCol5, noteCol5 = ols_data(chartid5)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d5 = today.strftime("%Y-%m-01")

    dfcsv5['YM'] = dfcsv5[dateCol5]
    dfcsv5["YM"] = pd.to_datetime(dfcsv5["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv5['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv5 = pd.merge(all_dates, dfcsv5, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv5['nameColcusum5'] = dfcsv5[nameCol5] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv5['Mean']= dfcsv5['nameColcusum5'].mean()
    
    
#=====================================================================   #AC New and Existing
     
        
    chartid6 = 52
    row6 =6
    dfcsv6, nameCol6, dateCol6, title6, conf_limit6, formatCol6, noteCol6 = ols_data(chartid6)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d6 = today.strftime("%Y-%m-01")

    dfcsv6['YM'] = dfcsv6[dateCol6]
    dfcsv6["YM"] = pd.to_datetime(dfcsv6["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv6['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv6 = pd.merge(all_dates, dfcsv6, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv6['nameColcusum6'] = dfcsv6[nameCol6] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv6['Mean']= dfcsv6['nameColcusum6'].mean()
    
   
    
#=====================================================================   #SM New and Existing #7
     
        
    chartid7 = 53
    row7 =7
    dfcsv7, nameCol7, dateCol7, title7, conf_limit7, formatCol7, noteCol7 = ols_data(chartid7)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d7 = today.strftime("%Y-%m-01")

    dfcsv7['YM'] = dfcsv7[dateCol7]
    dfcsv7["YM"] = pd.to_datetime(dfcsv7["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv7['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv7 = pd.merge(all_dates, dfcsv7, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv7['nameColcusum7'] = dfcsv7[nameCol7] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv7['Mean']= dfcsv7['nameColcusum7'].mean()
    
    
        
#=====================================================================   #AC Quotes #8
     
        
    chartid8 = 97
    row8 =8
    dfcsv8, nameCol8, dateCol8, title8, conf_limit8, formatCol8, noteCol8 = ols_data(chartid8)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d8 = today.strftime("%Y-%m-01")

    dfcsv8['YM'] = dfcsv8[dateCol8]
    dfcsv8["YM"] = pd.to_datetime(dfcsv8["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv8['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv8 = pd.merge(all_dates, dfcsv8, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv8['nameColcusum8'] = dfcsv8[nameCol8] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv8['Mean']= dfcsv8['nameColcusum8'].mean()
    
    
            
#=====================================================================   #SM Quotes #9
     
        
    chartid9 = 98
    row9 =9
    dfcsv9, nameCol9, dateCol9, title9, conf_limit9, formatCol9, noteCol9 = ols_data(chartid9)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
#     d9 = today.strftime("%Y-%m-01")

    dfcsv9['YM'] = dfcsv9[dateCol9]
    dfcsv9["YM"] = pd.to_datetime(dfcsv9["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv9['YM'].min(),end=end_date_of_last_month,freq="MS")})
    
    dfcsv9 = pd.merge(all_dates, dfcsv9, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv9['nameColcusum9'] = dfcsv9[nameCol9] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv9['Mean']= dfcsv9['nameColcusum9'].mean()
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    

    fig = make_subplots(rows=9, cols=1 , row_heights=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1],   subplot_titles = ("Quotes(88)","New and Existing Sales(50)","Total Maintenance(96)", "AC Maintenenace(71)","SM Maintenance(61)", "AC New and Existing(52)", "SM New and Existing(53)", "AC Quotes (97)", "SM Quotes (98)"))
    # row_heights=[0.16, 0.16, 0.16, 0.16, 0.16, 0.16],
    # vertical_spacing= 0.16, 
#======================================================= quotes row 1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv1['Mov_avg8'],
                          mode='lines',
                          name='Quotes New and Existing per month',
                          line=dict(
        color=('green'),
        width=2,
        ),
        visible=True),
        row=row1, col=1)
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv1['Mean'] ,
                          mode='lines',
                          name='Quotes New and Existing average',
                          line=dict(
        color=('green'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row1, col=1)
    
    
#===================================================== New and Existing Sales row 2    
    #New and Existing Sales row 2
    
    fig.add_trace(go.Scatter(x=dfcsv2[dateCol2],
                         y = dfcsv2['Mov_avg8'],
                          mode='lines',
                          name='Sales New and Existing per month"',
                          line=dict(
        color=('blue'),
        width=2,
        ),
        visible=True),
        row=row2, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv2[dateCol2],
                         y = dfcsv2['Mean'] ,
                          mode='lines',
                          name='Sales New and Existing average',
                          line=dict(
        color=('blue'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row2, col=1)
    
# ====================================================================  Total Maint row 3  
    #Total Maint row 3
    fig.add_trace(go.Scatter(x=dfcsv3[dateCol3],
                         y = dfcsv3['Mov_avg8'],
                          mode='lines',
                          name='Total Maintenance',
                          line=dict(
        color=('brown'),
        width=2,
        ),
        visible=True),
        row=row3, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv3[dateCol3],
                         y = dfcsv3['Mean'] ,
                          mode='lines',
                          name='Total Maintenance average',
                          line=dict(
        color=('brown'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row3, col=1)
    
#================================================================    AC Maint row 4
    
    #AC Maint row 4
    fig.add_trace(go.Scatter(x=dfcsv4[dateCol4],
                         y = dfcsv4['Mov_avg8'],
                          mode='lines',
                          name='AC Maintenance',
                          line=dict(
        color=('brown'),
        width=2,
        ),
        visible=True),
        row=row4, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv4[dateCol4],
                         y = dfcsv4['Mean'] ,
                          mode='lines',
                          name='AC Maintenance average',
                          line=dict(
        color=('brown'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row4, col=1)
        
#===================================================================== M Maint row 5     
    
#SM Maint row 5
    fig.add_trace(go.Scatter(x=dfcsv5[dateCol5],
                         y = dfcsv5['Mov_avg8'],
                          mode='lines',
                          name='SM Maintenance',
                          line=dict(
        color=('brown'),
        width=2,
        ),
        visible=True),
        row=row5, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv5[dateCol5],
                         y = dfcsv5['Mean'] ,
                          mode='lines',
                          name= 'SM Maintenance average',
                          line=dict(
        color=('brown'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row5, col=1)
    
#===================================================================== M AC New and Existing row 6      

    fig.add_trace(go.Scatter(x=dfcsv6[dateCol6],
                         y = dfcsv6['Mov_avg8'],
                          mode='lines',
                          name='AC New and Existing',
                          line=dict(
        color=('blue'),
        width=2,
        ),
        visible=True),
        row=row6, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv6[dateCol6],
                         y = dfcsv6['Mean'] ,
                          mode='lines',
                          name= 'AC New and Existing average',
                          line=dict(
        color=('blue'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row6, col=1)

 #=====================================================================  SM New and Existing row 7     

    fig.add_trace(go.Scatter(x=dfcsv7[dateCol7],
                         y = dfcsv7['Mov_avg8'],
                          mode='lines',
                          name='SM New and Existing',
                          line=dict(
        color=('blue'),
        width=2,
        ),
        visible=True),
        row=row7, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv7[dateCol7],
                         y = dfcsv7['Mean'] ,
                          mode='lines',
                          name= 'SM New and Existing average',
                          line=dict(
        color=('blue'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row7, col=1)   
    
  #=====================================================================  AC Quotes row 8    

    fig.add_trace(go.Scatter(x=dfcsv8[dateCol8],
                         y = dfcsv8['Mov_avg8'],
                          mode='lines',
                          name='AC Quotes',
                          line=dict(
        color=('green'),
        width=2,
        ),
        visible=True),
        row=row8, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv8[dateCol8],
                         y = dfcsv8['Mean'] ,
                          mode='lines',
                          name= 'AC Quotes average',
                          line=dict(
        color=('green'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row8, col=1)      
    
    
   #=====================================================================  SM Quotes row 9    

    fig.add_trace(go.Scatter(x=dfcsv9[dateCol9],
                         y = dfcsv9['Mov_avg8'],
                          mode='lines',
                          name='SM Quotes',
                          line=dict(
        color=('green'),
        width=2,
        ),
        visible=True),
        row=row9, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv9[dateCol9],
                         y = dfcsv9['Mean'] ,
                          mode='lines',
                          name= 'SM Quotes average',
                          line=dict(
        color=('green'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=row9, col=1)    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#       #height
    fig.update_layout(height=1800, width=200, title_text= " Sales Sparklines based on a 12 month moving average (Chart id)")
    fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_annotations(font_size=12)
    # remove facet/subplot labels
#     fig.update_layout(annotations=[], overwrite=False)
    
  
    
    # strip down the rest of the plot
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        
    )
    
    # disable the modebar for such a small plot
    fig.show(config=dict(displayModeBar=False))
#     image = BlobMedia("image/png", pio.to_image(fig, format='png'), name="graph.png")
    return  fig
