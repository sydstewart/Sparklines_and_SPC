from ._anvil_designer import HomeTemplate
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
from ..Search_charts import Search_charts
from ..Form5 import Form5
from ..Test import Test
from .. import Globals
from datetime import datetime
from ..Stacked_Sales_Charts import Stacked_Sales_Charts
from ..Main_Account_users import Main_Account_users

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # login User
    anvil.users.login_with_form()
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']
    Globals.loggedin_user = loggedin_user
    Globals.organisation = organisation
    
    # load search charts form initially
    self.content_panel.clear()
    self.content_panel.add_component(Search_charts(), full_width_row=True)
    
    client = tz.tzlocal()
    Globals.offset = datetime.now(client).utcoffset().seconds 
       
    # #hyperlinks
    if get_url_hash() == 'Chart_form':
    
        self.content_panel.clear()
        self.content_panel.add_component(Chart_form(), full_width_row=True)
    elif get_url_hash() == 'Form1':
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)
    elif get_url_hash() == 'support_sparklines':
        self.content_panel.clear()
        self.content_panel.add_component(support_sparklines(), full_width_row=True)
    elif get_url_hash() == 'Stacked_Sales_charts':
        self.content_panel.clear()
        self.content_panel.add_component(Stacked_Sales_charts(), full_width_row=True)
  
  def reset_links(self, **event_args):
    self.link_3.role = ''
    self.link_2.role = ''      

  # Search Menu  
  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.reset_links()
    self.link_3.role = 'selected'

    self.content_panel.clear()
    self.content_panel.add_component(Search_charts(), full_width_row=True)
    self.reset_links()
    pass
    
    
  # New Chart form   
  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.reset_links()
    self.link_2.role = 'selected'

    self.content_panel.clear()
#     self.content_panel.add_component(Chart_form(), full_width_row=True)
    new_chart = {}
    # Open an alert displaying the 'Chart_form' Form
    save_clicked = alert(
      content=Chart_form(item=new_chart),
      title="Add Chart",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )

    # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      anvil.server.call('add_chart', new_chart)
    self.reset_links()
    pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.reset_links()
    self.link_1.role = 'selected'
    anvil.server.call('last_date_update_background')
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('get_chart_background')
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.reset_links()
    self.link_5.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Main_Account_users(), full_width_row=True)
    self.reset_links()   

    pass

  # stacked Sales Charts
  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.reset_links()
    self.link_6.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Stacked_Sales_Charts(), full_width_row=True)
    self.reset_links()
    pass




  




