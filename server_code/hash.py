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
def SH1Hash(name):
  
  import hashlib
  import xml.etree.ElementTree as ET
  
  myhash = hashlib.sha1(name.encode('utf-8'))
  myhash = myhash.hexdigest()
  myhash =str(myhash)
  return myhash

