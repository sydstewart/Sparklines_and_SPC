import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable    
def find_users_in_organisation(loggedin_user):
    loggedin_user = anvil.users.get_user()
    loggedin_user_email = loggedin_user['email']
    loggedin_user_org = loggedin_user['Organisation']['OrganisationName']
    print('Logged in User=',loggedin_user_email)
    print('Logged in User Org=',loggedin_user_org)
  #find organisation of logged in user
    org = app_tables.organisation.get(Main_email=loggedin_user)
#   for row in org: 
#         print('Org Name=',row['Main_email'])
#   if org != None:
    associated_users = app_tables.users.search(Organisation = org)
    for row in associated_users:
         print(row['email'])
        
    return associated_users
        
        
        
@anvil.server.callable
def add_user(new_user_dict):
  loggedin_user = anvil.users.get_user()
  app_tables.users.add_row(
    Invited_date_time=datetime.now(),
    Organisation = loggedin_user['Organisation'],
    **new_user_dict
  )
