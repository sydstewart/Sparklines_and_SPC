from ._anvil_designer import searchesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, time
from anvil import tz
from .. import Globals

class searches(searchesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    from .. import Globals
    client = tz.tzlocal()
    print('client in AC', client)
    Globals.offset = datetime.now(client).utcoffset().seconds
    print('offset_AC', Globals.offset)
  
    Organisation = app_tables.organisation.get(id = 1)
    User = app_tables.users.get(email = 'sydney.w.stewart@gmail.com')
    print('User',User)
    folders = [(cat ['folder_name'], cat) for cat in app_tables.folders.search(Organisation = Organisation)]
    # Any code you write here will run when the form opens.
    self.drop_down_1.items = folders

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    then = datetime.now()
    folder_row = self.drop_down_1.selected_value
    print('selected_folder_row',folder_row)
    folder = folder_row['folder_name']
    print('selected_folder',folder)
    loggedin_user = anvil.users.get_user()
    user_type = Globals.user_type 
    chart_rows =anvil.server.call('get_charts_simple',folder_row)
    self.repeating_panel_1.items = chart_rows
         
    print("Dropdown Search Time: " + str(datetime.now() - then) + '\n')
    pass
    
 

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    then = datetime.now()
    chart_rows =anvil.server.call('get_charts_simple_text',self.text_box_1.text)
    self.repeating_panel_1.items = chart_rows
    print("Text Search Time: " + str(datetime.now() - then) + '\n')
    pass



