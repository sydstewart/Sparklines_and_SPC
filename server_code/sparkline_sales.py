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
from datetime import date
from plotly.subplots import make_subplots
import plotly.io as pio
from anvil import BlobMedia

@anvil.server.callable
def get_sparklines_sales():
    
    #quotes
    chartid1 = 88
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1, noteCol1 = ols_data(chartid1)
    
    # create a dataframe for all_dates with Nan entries between the start date and today
    today = date.today()
    d1 = today.strftime("%Y-%m-01")
    dfcsv1['YM'] = dfcsv1[dateCol1]
    dfcsv1["YM"] = pd.to_datetime(dfcsv1["YM"]) 
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv1['YM'].min(),end=d1,freq="MS")})
    
    dfcsv1 = pd.merge(all_dates, dfcsv1, how="left", on='YM').fillna(0)
    
    # Calculate cusums   
    dfcsv1['nameColcusum1'] = dfcsv1[nameCol1] 
#     dfcsv1['nameColavg1'] = dfcsv1['nameColcusum1'].rolling(window=21).mean() 
#     dfcsv1['nameColcusum1'] = dfcsv1['nameColcusum1'].cumsum()
   # calculate mean
    dfcsv1['Mean']= dfcsv1[nameCol1].mean()
    
    # New and Exosting Sales
    chartid2 = 50
    
    
    dfcsv2, nameCol2, dateCol2, title2, conf_limit2, formatCol2, noteCol2  = ols_data(chartid2)
    
    all_dates = pd.DataFrame({"YM":pd.date_range(start=dfcsv2['YM'].min(),end=d1,freq="MS")})
    dfcsv2['YM'] = dfcsv2[dateCol2]
    dfcsv2["YM"] = pd.to_datetime(dfcsv2["YM"])
    
    dfcsv2 = pd.merge(all_dates, dfcsv2, how="left", on='YM').fillna(0)
    
    dfcsv2['nameColcusum2'] = dfcsv2[nameCol2]
    
    # calculate mean
    dfcsv2['Mean']= dfcsv2[nameCol2].mean()
    
#     dfcsv2['nameColcusum2'] = dfcsv2['nameColcusum2'].cumsum()
    
#     chartid3 = 74
#     dfcsv3, nameCol3, dateCol3, title3, conf_limit3, formatCol3 = ols_data(chartid3)
#     dfcsv3['YM'] = dfcsv3[dateCol3]
#     dfcsv3["YM"] = pd.to_datetime(dfcsv3["YM"])
    
#     dfcsv3 = pd.merge(all_dates, dfcsv3, how="left", on='YM').fillna(0)
   
#     dfcsv3['nameColcusum3'] = dfcsv3[nameCol3] 
# #     dfcsv3['nameColcusum3'] = dfcsv3['nameColcusum3'].cumsum()
    
#     chartid4 = 75
#     dfcsv4, nameCol4, dateCol4, title4, conf_limit4, formatCol4 = ols_data(chartid4)
#     dfcsv4['YM'] = dfcsv4[dateCol4]
#     dfcsv4["YM"] = pd.to_datetime(dfcsv4["YM"])
    
#     dfcsv4 = pd.merge(all_dates, dfcsv4, how="left", on='YM').fillna(0)
   
#     dfcsv4['nameColcusum4'] = dfcsv4[nameCol4] 
# #     dfcsv4['nameColcusum4'] = dfcsv4['nameColcusum4'].cumsum()
 
    fig = make_subplots(rows=3, cols=1 , row_heights=[0.34, 0.33, 0.33],)# subplot_titles = ("Defect Change Notes","Improvement Change Notes","RCA actions completed"))
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv1[nameCol1],
                          mode='lines',
                          name='Quotes New and Existing per month',
                          line=dict(
        color=('green'),
        width=2,
        ),
        visible=True),
        row=1, col=1)
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
        row=1, col=1)
    
    
    
    
    
    fig.add_trace(go.Scatter(x=dfcsv2[dateCol2],
                         y = dfcsv2[nameCol2],
                          mode='lines',
                          name='Sales New and Existing per month"',
                          line=dict(
        color=('blue'),
        width=2,
        ),
        visible=True),
        row=2, col=1) 
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv2['Mean'] ,
                          mode='lines',
                          name='Sales New and Existing average',
                          line=dict(
        color=('blue'),
        width=1,
         dash='dash'                   
        ),
        visible=True),
        row=2, col=1)
#     fig.add_trace(go.Scatter(x=dfcsv3[dateCol3],
#                          y = dfcsv3[nameCol3],
#                           mode='lines',
#                           name='RCA Actions completed',
#                           line=dict(
#         color=('orange'),
#         width=2,
#         ),
#         visible=True),
#         row=3, col=1) 
    
#       #height
    fig.update_layout(height=200, width=200, title_text= " Sales Sparklines")
    fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    
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
