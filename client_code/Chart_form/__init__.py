from ._anvil_designer import Chart_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from . import Globals

class Chart_form(Chart_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_4.visible = False
    self.data_grid_1.visible = False
    self.text_box_4.visible = False
    
    
    
    organisation = app_tables.organisation.get(id = 1)
    
    # get folders
    folders = [
    (cat['folder_name'], cat) for cat in app_tables.folders.search(tables.order_by('folder_name', ascending=True), Organisation = organisation)
     ]
    self.drop_down_1.items = folders
    print(folders)
    # get filenames
    filenames = [(cat['name'], cat) for cat in app_tables.my_files.search(tables.order_by('name', ascending=True), Organisation = organisation)]
    self.drop_down_2.items= filenames
    # Any code you write here will run when the form opens.
    
    # get column names for selected file
     
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Form1')
    pass

  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    fileName = self.drop_down_2.selected_value
#     fileName = fileName['name']
    columns = anvil.server.call('chart_columns',fileName)
    self.drop_down_4.items = columns
    self.drop_down_3.items = ['YM', 'DefectCount', 'ImprovementCount','syd']
    pass

  def drop_down_4_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def drop_down_3_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def text_box_2_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    fileName = self.drop_down_2.selected_value
#     fileName = fileName['name']
    columns = anvil.server.call('chart_columns',fileName)
    valid = anvil.server.call('search_columns', columns, self.text_box_2.text)
    if valid == False:
        self.text_box_4.visible = True
        self.text_box_2.text =''
    elif valid == True: 
        self.text_box_4.visible = False
    pass





