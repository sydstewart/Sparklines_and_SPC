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
    self.text_box_3.text = ''
    
    
    # setup globals
    global folderselected , displayEdit
    folder =self.folder_search_drop_down.selected_value
    if folder is not None:
        Globals.folderselected = folder['Folder']
    else:
        alert(' Enter a Folder!')
    
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
    self.text_box_3.text = ''
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

  def archive_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.text_box_1.text = ''
    self.text_box_2.text = 0
#     then_start =  datetime.now()
    global folderselected , displayEdit
    folder =self.folder_search_drop_down.selected_value
    if folder is not None:
        Globals.folderselected = folder['Folder']
   
      
    #     then =  datetime.now()
        loggedin_user = anvil.users.get_user()
    #     print("Client get user Time: " + str(datetime.now() - then) + '\n')
        
        # Note: needs 'UserdisplayEdit' to control edit buttons on charts displayed
    #     then =  datetime.now()
        UserdisplayEdit, chart_rows = anvil.server.call('display_charts', Globals.folderselected, loggedin_user, archive = self.archive_chkbox.checked)
    #     print("Client combined useraccess and chartrows Time: " + str(datetime.now() - then) + '\n')
        
        Globals.displayEdit =UserdisplayEdit
    #     print ('Folder selected=',folder['Folder']['folder_name'])
    #     then =  datetime.now()
    #     UserdisplayEdit = anvil.server.call('check_acccess_level', Globals.folderselected, loggedin_user)
    #     print("Client check_access_level call Time: " + str(datetime.now() - then) + '\n')
    

    
#     then =  datetime.now() 
#     chart_rows= anvil.server.call('get_data_by_folder', folder, archive = self.archive_chkbox.checked)
#     print("Client get_data_by_folder Time: " + str(datetime.now() - then) + '\n')

#     chart_rows= app_tables.charts.search(folder_name = folder, archive = archive  )
#     then =  datetime.now()
        hits = len(chart_rows)
        self.text_box_2.text = hits
  #     print('Hits=', hits)
        self.repeating_panel_1.items=chart_rows
    else:
        alert('Enter a Folder!')
    pass
   
#chartid entered
  def text_box_3_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.folder_search_drop_down.visible = False 

    if self.text_box_1.text == '':
         self.folder_search_drop_down.visible = True 
        
    # Note: needs 'UserdisplayEdit' to control edit buttons on charts displayed
    UserdisplayEdit, chart_rows = anvil.server.call('display_charts_from_chartid', self.text_box_3.text, Globals.loggedin_user, archive = self.archive_chkbox.checked)

    Globals.displayEdit =UserdisplayEdit

    self.repeating_panel_1.items=chart_rows
    
    hits = len(chart_rows)
    self.text_box_2.text = hits
    
    self.folder_search_drop_down.visible = True

  pass

  


