from ._anvil_designer import stacked_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stacked_form(stacked_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    folders = [(cat['folder_name'], cat) for cat in app_tables.folders.search()     ]
    self.drop_down_1.items = folders
    # Any code you write here will run when the form opens.