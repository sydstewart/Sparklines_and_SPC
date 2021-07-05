import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from datetime import datetime , timedelta

@anvil.server.callable
def add_chart(chart_dict):
  print(chart_dict)
  max_value = app_tables.charts.search(tables.order_by("id", ascending=False))[0]['id']
  max_value = max_value + 1     
  current_user = anvil.users.get_user()
  bootnum,backBootnum = anvil.server.call('get_default_bootnums') 
  
  app_tables.charts.add_row(**chart_dict,id = max_value,updated_last = datetime.now(), archive = False,End_date_Overwrite = False, bootnum = bootnum, backBootnum = backBootnum)

  
@anvil.server.callable
def get_default_bootnums():
   loggedinUser = anvil.users.get_user()
   organisation = loggedinUser['Organisation']
   orgid = organisation['id']
   t = app_tables.organisation.get(id = orgid)
   bootnum = t['BootNumDefault']
   backBootnum =t['backgrBootnum']
   return bootnum,backBootnum
  
@anvil.server.callable  
def save_test(newtest):
     print(newtest)
     app_tables.test.add_row(**newtest)
  