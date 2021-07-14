from ._anvil_designer import FolderChartUserAccessTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Folder_Shares_Card import Folder_Shares_Card
 


class FolderChartUserAccess(FolderChartUserAccessTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    loggedin_user = anvil.users.get_user()
    # Any code you write here will run when the form opens.
    organisation = loggedin_user['Organisation']
    
    folders = [(cat['folder_name'], cat) for cat in app_tables.folders.search(Organisation = organisation)]
    self.folder_search_dropdown.items = folders
   
    users = [(cat['email'], cat) for cat in app_tables.users.search(Organisation = organisation)]
    self.user_search_dropdown.items = users
    
    charts = [(cat['title'], cat) for cat in app_tables.charts.search(Organisation = organisation)]
    self.chart_search_dropdown.items = charts
    
    
    folderfilter = self.folder_search_dropdown.selected_value
    userfilter = self.user_search_dropdown.selected_value
    accessfilter = self.access_dropdown.selected_value
    chartfilter = self.chart_search_dropdown.selected_value
    
    self.repeating_panel_1.items = anvil.server.call('get_data_by_folderChartUser',loggedin_user,folderfilter, userfilter, accessfilter, chartfilter)
   


  def add_new_shared_user_button_click(self, **event_args):
    # Initialise an empty dictionary to store the user inputs
    new_shared_user = {}

    save_clicked = alert(
      content=Folder_Shares_Card(item=new_shared_user),
      title="Add Shared User",
      large=True,
      buttons=[("Save", True), ("Cancel", False)],
    )
    # If the alert returned 'True', the save button was clicked.
#     print('new_shared_user=',content)
#     folder = self.folder_drop_down.s
#     access_level = new_shared_user['AccessLevel']
    if save_clicked:

        dup = anvil.server.call('check_shared_user_duplicate',new_shared_user)
        print('dup=', dup)
        if dup == 0:
              anvil.server.call('add_shared_user', new_shared_user)
        else:
          alert('This is a duplicate record')
#           # Now refresh the page
    self.refresh_folder_shares()
    
          
  def refresh_folder_shares(self):
    # Load existing articles from the Data Table, and display them in the RepeatingPanel
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']
    folderfilter = self.folder_search_dropdown.selected_value
    userfilter = self.user_search_dropdown.selected_value
    self.repeating_panel_1.items = anvil.server.call('get_data_by_folderChartUser',loggedin_user,folderfilter, userfilter)
    print('refreshing')
    pass

  def goto_charts_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main_page')
    pass

    pass

  def folder_search_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']
    folderfilter = self.folder_search_dropdown.selected_value
    userfilter = self.user_search_dropdown.selected_value
    accessfilter = self.access_dropdown.selected_value
    chartfilter = self.chart_search_dropdown.selected_value
    self.repeating_panel_1.items = anvil.server.call('get_data_by_folderChartUser',loggedin_user,folderfilter, userfilter, accessfilter, chartfilter)
    pass

  def user_search_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']
    folderfilter = self.folder_search_dropdown.selected_value
    userfilter = self.user_search_dropdown.selected_value
    accessfilter = self.access_dropdown.selected_value
    chartfilter = self.chart_search_dropdown.selected_value
    self.repeating_panel_1.items = anvil.server.call('get_data_by_folderChartUser',loggedin_user,folderfilter, userfilter, accessfilter, chartfilter)
    pass
    

  def access_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    loggedin_user = anvil.users.get_user()
    organisation = loggedin_user['Organisation']
    folderfilter = self.folder_search_dropdown.selected_value
    userfilter = self.user_search_dropdown.selected_value
    accessfilter = self.access_dropdown.selected_value
    chartfilter = self.chart_search_dropdown.selected_value
    self.repeating_panel_1.items = anvil.server.call('get_data_by_folderChartUser',loggedin_user,folderfilter, userfilter, accessfilter, chartfilter)
    pass
 
  
  
  
  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main_Account_users')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Folders')
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('FolderChartUserAccess')
    pass
