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
from .control_charts import ols_data

def create_sparkline(chartid, rowno , color):
    
   
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1,noteCol = ols_data(chartid)

    # create a dataframe for all_dates with Nan entries javascript:void(0)between the start date and today
    today = date.today()
    d1 = today.strftime("%Y-%m-01")
    dfcsv1['Date_Entered'] = dfcsv1[dateCol1]
    dfcsv1["Date_Entered"] = pd.to_datetime(dfcsv1["Date_Entered"]) 
    
    # calculate mean
    dfcsv1['Mean']= dfcsv1[nameCol1].mean()
    mean1 = dfcsv1[nameCol1].mean()
    return mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1
    #add sparkline
#     fig = make_subplots(rows=3, cols=1 , row_heights=[0.34, 0.33, 0.33],)# subplot_titles = ("Defect Change Notes","Improvement Change Notes","RCA actions completed"))
    

@anvil.server.callable
def get_sparklines_changes():
    
   
    fig = make_subplots(rows=3, cols=1 , row_heights=[0.33, 0.33, 0.33 ], subplot_titles = ("Defects Detected (102)", \
                                                 "Improvement Changes (xxx)","All Changess (xxx)"))
   
  #================All Cases Arriving =========================================================================  
    chartid = 102
    rowno = 1
    color = 'blue'
    
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1  = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1['Mov_avg8'],
                          mode='lines',
                          name=name_of_chart,
                          line=dict(
        color=color,
        width=2,
        ),
        visible=True),
        row=rowno, col=1)
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1['Mean'] ,
                          mode='lines',
                          name= name_of_chart + ' ' + 'average  =' + str(round(mean1,0)),
                          line=dict(
        color=color,
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1) 
    
   
    fig.update_layout(height=100, width=200, title_text= "Product Change Sparklines (Chart Id)")
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
# #     image = BlobMedia("image/png", pio.to_image(fig, format='png'), name="graph.png")
    return  fig


