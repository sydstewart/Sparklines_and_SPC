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
def display_charts( folder, user, archive ):
   
    
    folder_share_rows= app_tables.folder_shares.search(Folder = folder,FolderUser = user)
  
     
    chart_rows= app_tables.charts.search(folder_name = folder, archive = archive  )

    
    return folder_share_rows ,chart_rows

@anvil.server.callable
def display_charts_from_textbox(text , user, archive ):
    user_type = user['user_type']

    text ='%' + text +'%'
     
    chart_rows = app_tables.charts.search(q.any_of(title=q.ilike(text)))

    return user_type,chart_rows