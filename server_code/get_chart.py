import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from .control_charts import ols_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go

@anvil.server.callable
def get_chart():
  
 
    
    chartid1 = 16
    dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1 = ols_data(chartid1)
    
    
    
    fig = make_subplots(rows=1, cols=1 , row_heights=[1])
    
    fig.add_trace(go.Scatter(
        x=dfcsv1[dateCol1],y= dfcsv1[nameCol1],
        hoverinfo='x+y',
        mode='markers+lines',
        name='Defect Change Notes',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        
    ))
    
    
    # Change grid color and axis colors
    # Change grid color and axis colors
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black') #, gridcolor='black')
    fig.update_yaxes(showline=True, linewidth=1)  #, linecolor='gray')
    fig.update_xaxes(tickangle= 45)
    fig.update_layout(plot_bgcolor='rgb(235, 240, 237)')
    fig.update_layout(height=1600, width=800, title_text=title1)
    return fig

