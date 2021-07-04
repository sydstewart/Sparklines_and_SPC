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
def get_all_charts():
  rows=app_tables.charts.search(title=q.ilike('No. of Cases%') )
  folder_rows = app_tables.folder_shares.search(AccessLevel=q.ilike('Designer') )
  rows = [dict(x) for x in rows]
  folder_rows = [dict(x) for x in folder_rows]
#   print(folder_rows)
  return rows, folder_rows

