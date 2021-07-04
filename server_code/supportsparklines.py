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
    
   
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = ols_data(chartid)

    # create a dataframe for all_dates with Nan entries between the start date and today
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
def get_sparklines_support():
    
   
    fig = make_subplots(rows=10, cols=1 , row_heights=[0.1, 0.1, 0.1, 0.1,0.1,0.1, 0.1, 0.1, 0.1,0.1],) # subplot_titles = ("Cases arriving per week","Improvement Change Notes","RCA actions completed"))
    
    chartid = 70
    rowno = 1
    color = 'blue'
    
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1  = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
    

    #Problem cases
    
    chartid = 44
    rowno = 2
    color = 'green'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color )
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv1[nameCol1],
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
    
    
    
    #config cases
    chartid = 45
    rowno = 3
    color = 'brown'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color )
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                         y = dfcsv1[nameCol1],
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
    
   
    #Interfaces
    
    chartid = 46
    rowno = 4
    color = 'red'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color=color,
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1) 
            # printing
    chartid = 33
    rowno = 5
    color = 'purple'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color=color,
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1)
    
    
    # how to
    chartid = 78
    rowno = 6
    color = 'black'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color=color,
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1) 
    
 # nps
    chartid = 51
    rowno = 7
    color = 'gold'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color='black',
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1)
    
 # nps response
    chartid = 79
    rowno = 8
    color = 'gold'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color='black',
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1)    

    # nps response
    chartid = 66
    rowno = 9
    color = 'maroon'
     
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1[nameCol1],
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
                          name= name_of_chart+ ' ' + 'average  = ' + str(round(mean1,0)),
                          line=dict(
        color='black',
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1) 
    
    
    fig.update_layout(height=200, width=200, title_text= " Support Sparklines")
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


         
          