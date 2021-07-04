import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server

@anvil.server.callable
def get_org():
    # some way to get it from the data table. obviously change as needed
     t = app_tables.organisation.get(id= 1)

     return t
