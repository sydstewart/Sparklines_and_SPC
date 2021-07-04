from ._anvil_designer import Home_pageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Home_page(Home_pageTemplate):
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
  
  def folder_search_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.text_box_1.text = ''
    
    # setup globals
    global folderselected , displayEdit
    folder =self.folder_search_drop_down.selected_value
    Globals.folderselected = folder['Folder']
    
    loggedin_user = anvil.users.get_user()

    # get charts for folder 
    UserdisplayEdit, chart_rows = anvil.server.call('display_charts', Globals.folderselected, loggedin_user, archive = self.archive_chkbox.checked)
    
    Globals.displayEdit =UserdisplayEdit

    hits = len(chart_rows)
    print('Hits=', hits)
    self.repeating_panel_1.items=chart_rows


