from ._anvil_designer import Search_chartsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Search_charts(Search_chartsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # login user
    anvil.users.login_with_form()
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']    
    
    # populate dropdown for Folder 
    folders = [(cat ['Folder']['folder_name'], cat) for cat in app_tables.folder_shares.search(FolderUser = loggedin_user, Organisation = organisation)]
    self.folder_search_drop_down.items = folders
  
  # search on dropdown selection
  def folder_search_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.text_box_1.text = ''
     
    
    
    # setup globals
    global folderselected , displayEdit
    folder =self.folder_search_drop_down.selected_value
    Globals.folderselected = folder['Folder']
    
    
    # get charts for folder 
    UserdisplayEdit, chart_rows = anvil.server.call('display_charts', Globals.folderselected, Globals.loggedin_user, archive = self.archive_chkbox.checked)
    
    Globals.displayEdit =UserdisplayEdit

    hits = len(chart_rows)
    self.text_box_2.text = hits
    self.repeating_panel_1.items=chart_rows

  # text search box on pressing enter
  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
         
    self.folder_search_drop_down.visible = False 

    if self.text_box_1.text == '':
         self.folder_search_drop_down.visible = True 
        
    # Note: needs 'UserdisplayEdit' to control edit buttons on charts displayed
    UserdisplayEdit, chart_rows = anvil.server.call('display_charts_from_textbox', self.text_box_1.text, Globals.loggedin_user, archive = self.archive_chkbox.checked)

    Globals.displayEdit =UserdisplayEdit

    self.repeating_panel_1.items=chart_rows
    
    hits = len(chart_rows)
    self.text_box_2.text = hits
    
    self.folder_search_drop_down.visible = True

  pass
