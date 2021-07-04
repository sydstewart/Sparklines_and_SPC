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
from ..Chart_form import Chart_form
from ..Form1 import Form1
from ..support_sparklines import support_sparklines
from ..Home_page import Home_page
from ..Form5 import Form5

class Form4(Form4Template):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if get_url_hash() == 'Chart_form':
    
        self.content_panel.clear()
        self.content_panel.add_component(Chart_form(), full_width_row=True)
    elif get_url_hash() == 'Form1':
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)
    elif get_url_hash() == 'support_sparklines':
        self.content_panel.clear()
        self.content_panel.add_component(support_sparklines(), full_width_row=True)
         
    # Any code you write here will run when the form opens.
    
  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Home_page(), full_width_row=True)
    pass
    
    
    
  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Chart_form(), full_width_row=True)
    pass
  
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(support_sparklines(),full_width_row=True)
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form5(),full_width_row=True)
    pass
   


