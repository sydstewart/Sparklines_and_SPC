from ._anvil_designer import Change_Notes_DefectTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Change_Notes_Defect(Chane_Notes_DefectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    media_obj = anvil.server.call('getsheet')
    self.image_1.source = media_obj
    # Any code you write here will run when the form opens.
    
