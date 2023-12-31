from ._anvil_designer import RowTemplate8Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Chart_form import Chart_form 
from datetime import datetime

class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.plot_1.visible = False
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
  
# Select Charts
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    from ...Chart_Types import charts , trends , step_changes, tables, range, range_cusum, chart_cusum
    if self.drop_down_1.selected_value == "Chart":
          charts(self)
    if self.drop_down_1.selected_value == "Chart Cusum":
          chart_cusum(self)
    if self.drop_down_1.selected_value == "Range":
          range(self)
    if self.drop_down_1.selected_value == "Range Cusum":
          range_cusum(self)
    if self.drop_down_1.selected_value == "Trend":
          trends(self)

    if self.drop_down_1.selected_value == "Step change":
          startstep = datetime.now()
          chart_position = 1
          step_changes(self,chart_position)
#           print("Step Change total Time: " + str(datetime.now() - startstep) + '\n')
    if self.drop_down_1.selected_value == "Show Data":
          self.plot_1.visible = True 
          chart_copy = dict(list(self.item))
          chartid = chart_copy['id']
          filename = chart_copy['file_name']['name']
          print('filename=',filename)
          data = anvil.server.call('showdata',chartid, filename) 
          self.plot_1.data = data
    if self.drop_down_1.selected_value == "Hide":           
             self.plot_1.visible = False     
    pass
  
# conf Level dropdown
  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    from ...Chart_Types import charts , trends , step_changes, tables
    chart_position = 1
    stepchangeStart = datetime.now()
    step_changes(self,chart_position)
  
    pass
    

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    chart_copy = dict(list(self.item))
    chartid = chart_copy['id']
    anvil.server.call('get_chart_background_individual', chartid)
    pass
   

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.refresh_data_bindings()
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    from ...Chart_Types import charts , trends , step_changes, tables, range,range_cusum, chart_cusum
    if self.drop_down_1.selected_value == "Chart":
          charts(self)
    if self.drop_down_1.selected_value == "Range":
          range(self)
    if self.drop_down_1.selected_value == "Range Cusum":
          range_cusum(self)
    if self.drop_down_1.selected_value == "Chart Cusum":
          chart_cusum(self)
    if self.drop_down_1.selected_value == "Trend":
          trends(self)
    if self.drop_down_1.selected_value == "Step change":
          startstep = datetime.now()
          chart_position = 1
          step_changes(self,chart_position)
#           print("Step Change total Time: " + str(datetime.now() - startstep) + '\n')
    if self.drop_down_1.selected_value == "Show Data":
          self.plot_1.visible = True 
          chart_copy = dict(list(self.item))
          chartid = chart_copy['id']
          filename = chart_copy['file_name']['name']
          print('filename=',filename)
          data = anvil.server.call('showdata',chartid, filename) 
          self.plot_1.data = data
    if self.drop_down_1.selected_value == "Hide":           
             self.plot_1.visible = False 
    pass

  def dup_chart_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    chart_copy = dict(list(self.item))
    anvil.server.call('duplicate_chart',chart_copy)
    self.refresh_data_bindings()
    pass

  # start date changed
  def date_picker_1_change(self, **event_args):
    """This method is called when the selected date changes"""
    from ...Chart_Types import charts , trends , step_changes, tables, range, range_cusum
    if self.drop_down_1.selected_value == "Hide":
        alert('Please first select Chart Type')
    if self.drop_down_1.selected_value == "Chart":
          charts(self)
    if self.drop_down_1.selected_value == "Range":
          range(self)
    if self.drop_down_1.selected_value == "Trend":
          trends(self)
    if self.drop_down_1.selected_value == "Step change":
          startstep = datetime.now()
          chart_position = 1
          step_changes(self,chart_position)
#           print("Step Change total Time: " + str(datetime.now() - startstep) + '\n')
    if self.drop_down_1.selected_value == "Show Data":
          self.plot_1.visible = True 
          chart_copy = dict(list(self.item))
          chartid = chart_copy['id']
          filename = chart_copy['file_name']['name']
          print('filename=',filename)
          data = anvil.server.call('showdata',chartid, filename) 
          self.plot_1.data = data
    if self.drop_down_1.selected_value == "Hide":           
             self.plot_1.visible = False    
    pass

  # def date_picker_2_change(self, **event_args):
  #   """This method is called when the selected date changes"""

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def date_picker_3_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass

  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass
    





