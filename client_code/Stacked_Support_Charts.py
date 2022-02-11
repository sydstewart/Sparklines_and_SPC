from ._anvil_designer import Stacked_Support_ChartsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Chart_Types import create_chart, create_step_chart
class Stacked_Support_Charts(Stacked_Support_ChartsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    chartid = 95
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 1
    create_step_chart(self,chart_copy, chart_position)
    
        
    
    chartid = 44
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 2
    create_step_chart(self,chart_copy, chart_position)
    
    chartid = 45
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position =3
    create_step_chart(self,chart_copy, chart_position)
    
#     chartid = 100
#     chart_copy = app_tables.charts.get(id = chartid) 
#     print(chart_copy['id'])
#     chart_position = 4
#     create_step_chart(self,chart_copy, chart_position)
    
    chartid = 46
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 4
    create_step_chart(self,chart_copy, chart_position)
    
    chartid = 47
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 5
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 78
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position =6
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 51
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 7
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 79
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 8
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 66
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 9
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    

    
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email_sales_step_changes_background')
    pass

