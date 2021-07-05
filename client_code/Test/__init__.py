from ._anvil_designer import TestTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Test(TestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""

    thisdict = [('Hello',5)]

    self.drop_down_1.items = thisdict
    newtest = {}
    # Open an alert displaying the 'Chart_form' Form
    save_clicked = alert(
      content=Test(item=newtest),
      title="Add Test",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )

    # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      anvil.server.call('save_test', newtest)

    
    
    pass

