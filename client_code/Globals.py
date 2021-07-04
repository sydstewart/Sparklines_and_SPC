import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import datetime
from anvil import tz

# offset = offset
# client = tz.tzlocal()
# print('client', client)
 
# # offset= offset
# print('globals_offset', offset)
# # client = tz.tzlocal()
# # print('client', client)
# # offset = datetime.now(client).utcoffset().seconds

# # print('offset', offset)
# # # Globals.offset = anvil.server.call('what_time',offset=offset)