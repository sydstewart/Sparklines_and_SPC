import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import anvil.tz
import anvil.tz
from datetime import datetime, timedelta, timezone
from anvil import tz

@anvil.server.callable
def what_time(offset):
  client = tz.tzlocal()
  offset = datetime.now(client).utcoffset().seconds
  print('offset from what_time', offset)
  now = datetime.now(client)
  print('now from what_time ',now)
  return now

@anvil.server.callable
def time_format():
    from datetime import datetime ,timedelta, date
    hoursoffset = 1
  
    naive_local = datetime.now()
    # 2019-08-09 10:10:00.406000
    print('naive_local',naive_local)
    
    aware_local = datetime.now(anvil.tz.tzlocal())
    # 'stamped' with the timezone of the browser
    # 2019-08-09 10:10:00.418000+01:00
    print('aware_local',aware_local)
    
    naive_utc = datetime.utcnow()
    # 2019-08-09 09:10:00.426000
    print('naive_utc',naive_utc)
    
    aware_utc = datetime.now(anvil.tz.tzutc()) # note: NOT datetime.utcnow()
    # 'stamped' with the UTC timezone (timezone of the server)
    # 2019-08-09 09:10:00.433000+00:00
    print('aware_utc',aware_utc)
    
    bst_custom = datetime.now() + timedelta(hours=hoursoffset)
    # 'stamped' with the UTC+3 timezone
    # 2017-11-16 23:45:15+03:00
    print('bst_custom',bst_custom )
    
