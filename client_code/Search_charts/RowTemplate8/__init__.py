from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Chart_form import Chart_form 


class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    chart_copy = dict(list(self.item))
    print(chart_copy)
    
  
#     valid = False
     
    
#     while not valid:
    save_clicked = alert(
      content=Chart_form(item=chart_copy),
      title="Edit Chart",
      large=True,
      buttons=[("Update", True), ("Cancel", False)],
    )
      
      
       
      
#       if not save_clicked:
#         break
        
        
#       # validates all fields are present and correct  
#       if  (chart_copy['title'] !=  '') and (chart_copy['folder_name'] !=  None) \
#           and  (chart_copy['file_name'] !=  None) \
#           and (chart_copy['nameCol'] !=  '') and (chart_copy['dateCol'] !=  '')  \
#           and (chart_copy['astart_date'] != None) and (chart_copy['aend_date'] != None ) \
#           and (chart_copy['mov_avg'] !=  None) : 
#           valid = True
  

    if save_clicked :
#         alert("There is missing data - please complete the required fields")
#       else:
         
          anvil.server.call('update_chart', self.item, chart_copy)
#         alert("Record Updated")
    self.refresh_data_bindings()
    pass

