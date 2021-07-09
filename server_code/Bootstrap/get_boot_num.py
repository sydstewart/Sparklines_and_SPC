import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def setbootnum(bootnum, backbootnum):
    # some way to get it from the data table. obviously change as needed
     t = app_tables.charts.search()
     for row in t:
          row['bootnum'] = bootnum
          row['backBootnum'] = backbootnum
     return  



@anvil.server.callable
def get_boot_num(chartid):
    # some way to get it from the data table. obviously change as needed
#      print('Chartid=',chartid)
     t = app_tables.charts.get(id = chartid)
     bootnum = t['bootnum'] 
     backbootnum =  t['backBootnum'] 
     return  bootnum, backbootnum
