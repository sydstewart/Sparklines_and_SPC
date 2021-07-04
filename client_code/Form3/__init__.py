from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from datetime import datetime 
from anvil import tz

class Form3(Form3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    client = tz.tzlocal()
    print('client in AC', client)
    Globals.offset = datetime.now(client).utcoffset().seconds
    self.repeating_panel_1.items = anvil.server.call('get_items')
    anvil.server.call('convert_dict',self.repeating_panel_1.items, Globals.offset)
    # Any code you write here will run when the form opens.
    
