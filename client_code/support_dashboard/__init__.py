from ._anvil_designer import support_dashboardTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class support_dashboard(support_dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
#     self.image_2.visible = False
    self.plot_1.visible = True
    chartid = 70
    self.plot_1.figure = anvil.server.call('get_pdcalls_range', chartid)