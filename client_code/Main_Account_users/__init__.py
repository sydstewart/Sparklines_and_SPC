from ._anvil_designer import Main_Account_usersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..User_Card import User_Card

class Main_Account_users(Main_Account_usersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
       
    loggedin_user = anvil.users.get_user()
    loggedin_user_email = loggedin_user['email']
    self.users_associated.items = anvil.server.call('find_users_in_organisation', loggedin_user)
    
  def refresh_users(self):
    loggedin_user = anvil.users.get_user()
    # Load existing articles from the Data Table, and display them in the RepeatingPanel
    self.users_associated.items = anvil.server.call('find_users_in_organisation', loggedin_user)

  def add_user_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    new_user_dict = {}
    # Open an alert displaying the 'ArticleEdit' Form
    save_clicked = alert(
      content=User_Card(item=new_user_dict),
      title="Add New User",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
        # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      anvil.server.call('add_user', new_user_dict)

    self.refresh_users()
    pass


