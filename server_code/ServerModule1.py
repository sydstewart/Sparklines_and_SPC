import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from datetime import datetime

@anvil.server.callable
def duplicate_chart(chart_dict):
  max_value = app_tables.charts.search(tables.order_by("id", ascending=False))[0]['id']
  max_value = max_value + 1     
  current_user = anvil.users.get_user()
  chart_dict['id'] = max_value
  chart_dict['updated_last'] = datetime.now()
  chart_dict['archive'] = False
  chart_dict['End_date_Overwrite'] = False
  title = chart_dict['title']
  chart_dict['title'] = 'Duplicate record of ' + ' ' + title
  app_tables.charts.add_row(**chart_dict)