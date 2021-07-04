from ._anvil_designer import sales_sparklinesTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users 
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class sales_sparklines(sales_sparklinesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_1.visible = True
    fig = anvil.server.call('get_sparklines_sales')
    self.plot_1.figure = fig
#     media_object = anvil.server.call('create_zaphod_pdf')
#     anvil.media.download(media_object)
    # Any code you write here will run when the form opens.
    
       




#      anvil.server.call('send_pdf_email')
#      pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.button_1.visible = False
    media_object = anvil.server.call('create_zaphod_pdf')
    anvil.media.download(media_object)

    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email')
    pass



