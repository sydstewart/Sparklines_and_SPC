from ._anvil_designer import Stacked_Sales_ChartsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Chart_Types import create_chart, create_step_chart
class Stacked_Sales_Charts(Stacked_Sales_ChartsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    chartid = 88
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 1
    create_step_chart(self,chart_copy, chart_position)
    
    chartid = 50
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 2
    create_step_chart(self,chart_copy, chart_position)
    
    chartid = 96
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 3
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 71
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 4
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    
    chartid = 61
    chart_copy = app_tables.charts.get(id = chartid) 
    print(chart_copy['id'])
    chart_position = 5
    create_step_chart(self,chart_copy, chart_position)
    # Any code you write here will run when the form opens.
    