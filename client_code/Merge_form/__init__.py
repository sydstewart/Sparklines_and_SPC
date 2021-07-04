from ._anvil_designer import Merge_formTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Merge_form(Merge_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    rows = anvil.server.call('get_folders')
    self.folder_dropdown.items = rows
# # tables.order_by("folder_name", ascending = True)
#    return rows
#     rows= anvil.server.call('get_data_by_folder', folder, archive = self.archive_chkbox.checked)
#     self.repeating_panel_2.items=rows
#     charts = [(cat['name'], cat) for cat in app_tables.charts.search(Organisation = organisation)]
#     self.CSV_FILE_1_drop_down_1.items= charts
#     self.CSV_FILE_2_drop_down_2.items= charts
    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(self.CSV_FILE_1_drop_down_1.selected_value) 
    anvil.server.call('csv_data',self.CSV_FILE_1_drop_down_1.selected_value)
#     file2 = self.CSV_FILE_2_drop_down_2.selected_value
    
    pass

  def folder_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    pass


