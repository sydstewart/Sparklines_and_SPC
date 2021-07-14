from ._anvil_designer import Form4Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Chart_Types import create_chart
class Form4(Form4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    chartid = 90
    chart_copy = app_tables.charts.search(id = chartid) 
    print(chart_copy['id'])
    # Any code you write here will run when the form opens.
    
