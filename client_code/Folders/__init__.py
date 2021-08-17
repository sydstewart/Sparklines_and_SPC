from ._anvil_designer import FoldersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Folder_Card import Folder_Card


class Folders(FoldersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('get_folders')
    rows = anvil.server.call('get_folders_2')
    # Any code you write here will run when the form opens.
    self.repeating_panel_1.items = rows

  def add_new_folder_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    new_folder_dict = {}
    # Open an alert displaying the 'Category_formt' Form
    save_clicked = alert(
      content= Folder_Card(item=new_folder_dict),
      title="Add New Folder",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
#     print(new_category['name'])
#     newfolder = new_folder_dict['folder_name']
    # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      dup =  anvil.server.call('check_folder_not_exits_already', new_folder_dict)
      if dup == 0: 
            anvil.server.call('add_folder', new_folder_dict)
#             anvil.server.call('add_Folder_Share',new_folder_dict)
      else:
            alert( 'Folder is a Duplicate NOT saved')
        
#     self.repeating_panel_1.items = app_tables.folders.search()
    self.refresh_folders()
    pass
          
  def refresh_folders(self):
    # Load existing articles from the Data Table, and display them in the RepeatingPanel
    self.repeating_panel_1.items = anvil.server.call('get_folders_2')
    print('refreshing')
    pass
  


  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Main_page")
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main_Account_users')
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Folders')
    pass

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('FolderChartUserAccess')
    pass
