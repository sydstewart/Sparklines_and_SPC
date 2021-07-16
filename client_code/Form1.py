from ._anvil_designer import Form1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, time
from anvil import tz

from . import Module1

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    # Any code you write here will run when the form opens.
#     your_email_address = "shaun@anvil.works"
#     anvil.server.call('send_email', your_email_address)
    from . import Globals
    client = tz.tzlocal()
    print('client in AC', client)
    Globals.offset = datetime.now(client).utcoffset().seconds
    User = loggedin_user = anvil.users.get_user()
    Globals.loggedin_user = User
    Globals.user_type = User['user_type']
    print('Globals.user_type',Globals.user_type)
    print('offset_AC', Globals.offset)
    self.card_1.visible = False
    Organisation = app_tables.organisation.get(id = 1)
    User = app_tables.users.get(email = 'sydney.w.stewart@gmail.com')
    print('User',User)
    folders = [(cat ['Folder']['folder_name'], cat) for cat in app_tables.folder_shares.search(Organisation = Organisation, FolderUser = User)]
    self.drop_down_1.items = folders
    self.image_2.visible = True
    self.image_3.visible = False
    self.plot_2.visible = False
    self.plot_3.visible = False
    self.plot_4.visible = False
    self.plot_5.visible = False
    self.plot_6.visible = False
#     url_hash = get_url_hash()
#     if url_hash == 'sparklines':
#         new_panel = support_sparklines()
#         get_open_form().content_panel.clear()
#         get_open_form().content_panel.add_component(new_panel)
       
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    
    anvil.server.call('get_nps', Globals.offset)
    pass

  def button_2_click(self, **event_args):
    
    """This method is called when the button is clicked"""
    x_media =anvil.server.call("make_data")
    download(x_media)

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    filename ='nps.csv'
    chartid = 61
    data = anvil.server.call('tables', chartid, filename)
    self.table.visible = True
    self.table.data = data
    pass

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = 'sydney'
    myhash = anvil.server.call('SH1Hash',name)
    
    print(str(myhash))
    return str(myhash)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
#     anvil.server.call('get_statcounter', Globals.offset)
    anvil.server.call('get_DAS28_statcounter')
    pass

  def button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
#     client = tz.tzlocal()
#     print('client in AC', client)
#     Globals.offset = datetime.now(client).utcoffset().seconds
    print('offset_AC', Globals.offset)
    anvil.server.call('get_AC_statcounter',Globals.offset)
    pass

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    anvil.server.call('get_RH_statcounter', Globals.offset)
    pass

  def button_9_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('time_format')
    from . import Globals
    client = tz.tzlocal()
    print('client', client)
    offset = datetime.now(client).utcoffset().seconds
    Globals.offset = offset
    print('offset_DateTime', offset)
    
    pass

  def button_10_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.card_1.visible = True
    print('0) '+str(datetime.now()))
    self.repeating_panel_1.items = anvil.server.call('get_csvs')
    print('1) '+str(datetime.now()))
    pass

  def button_11_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.card_1.visible = False
    pass

  def button_12_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    anvil.server.call('get_projects_in_progress',Globals.offset)

  def button_13_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Merge_form')

  def button_14_click(self, **event_args):
    """This method is called when the button is clicked"""
    print('selected dropdown from foldershares', self.drop_down_1.selected_value) 
    print('0) '+str(datetime.now()))
    self.repeating_panel_2.items  = anvil.server.call('get_charts',self.drop_down_1.selected_value)
    print('1) '+str(datetime.now()))
#     self.drop_down_1.items = newlist
    pass

  def button_15_click(self, **event_args):
    """This method is called when the button is clicked"""
#     filename = 'nps.csv'
    scatter = anvil.server.call('turning_pts')
    self.plot_1.data = scatter
   

  def button_16_click(self, **event_args):
    """This method is called when the button is clicked"""
#     anvil.server.call('get_csv_data')
    self.image_1.source  = anvil.server.call('rdpexample')
    pass

  def button_17_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('get_csv_data')
    pass

  def button_18_click(self, **event_args):
    """This method is called when the button is clicked"""
    start_time=datetime.now()
#     rows, folder_rows =anvil.server.call('get_all_charts')
    
    print("Server Call Time: " + str( datetime.now() - start_time) + '\n')
    
       
    

    results = []
    for item in rows:
        results.append(item['title'])
        
    print(results)
    
    for i in rows:
       print (i['title'])
        
    for i in folder_rows:
       print (i['AccessLevel'])

    self.repeating_panel_3.items=folder_rows

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    
    chart_rows =anvil.server.call('get_charts', self.drop_down_1.selected_value)
    self.repeating_panel_2.items = chart_rows
    pass

  def button_19_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    
    anvil.server.call('get_nps_responses', Globals.offset)
    pass

  def button_20_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('searches')
    pass

  def button_21_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    EXCHR ="GBPUSD=X"
    anvil.server.call('get_usgb', Globals.offset, EXCHR)
    
    pass

  def button_22_click(self, **event_args):
    """This method is called when the button is clicked"""
    orgs = app_tables.organisation.get(id = 1)
#     for row in orgs:
#         print(row['OrganisationName'])
#         org = row['id']
    t = app_tables.charts.search()
    for charts in t:
      print(charts['title'])
      charts.update (Organisation = orgs)
    pass

  # update folder_shares table with chartids
  def button_23_click(self, **event_args):
    """This method is called when the button is clicked"""
    t = app_tables.charts.search()
    for charts in t:
        folder = charts['folder_name']['folder_name']
#         print(folder)
        folderrow = app_tables.folders.get(folder_name  = folder)
        print ('Folder Name =',folder)
        print(' chartid=', charts['id'])
        foldershares = app_tables.folder_shares.search(Folder=folderrow)
        for row in foldershares:
          print('AccessLevel=',row['AccessLevel'])
#         foldername = folder['folder_name']
#         folderrow = app_tables.folder_shares.get(Folder = foldername)
#         print(folderrow['folder_name'])
#         chartid = charts['id']
#         organisation =charts['Organisation']
#         print(organisation)
#         foldershares = app_tables.folder_shares.search(Folder=folderrow)
#         for fs in foldershares:
#           useremail = fs['FolderUser']['email']
#           print(useremail)
#     pass
   #MatLib control Charts
  def button_24_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_2.visible = False
    self.image_2.visible = True
    media_obj = anvil.server.call('control_charts')
    self.image_2.source = media_obj
#     self.download_link.url = media_obj
    pass

  #Plotly X and Mr Charts
  def plotly_x_chart_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.image_2.visible = False
    self.plot_2.visible = True
    chartid = 90
    self.plot_2.figure = anvil.server.call('get_pdcalls_range', chartid)
    
  #Improvements Stacked Plot
  def button_26_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_2.visible = True
    self.plot_2.figure = anvil.server.call('get_stacked_Improvements')
    pass
  
   #RCA Stacked Plot
  def button_27_click(self, **event_args):
    self.plot_2.visible = True
    self.plot_2.figure = anvil.server.call('get_stacked_RCA')
    pass
    pass
  
  #Stacked Chart Form
  def button_28_click(self, **event_args):
    """This method is called when the button is clicked"""
  
    from .stacked_form import stacked_form
    # Initialise an empty dictionary to store the user inputs
    new_stacked_chart = {}
    # Open an alert displaying the 'ArticleEdit' Form
#     if self.category_box.selected_value is None:
#        alert('Enter a Category')
    save_clicked = alert(
      content=stacked_form(item=new_stacked_chart),
      title="Add Stacked Chart",
      large=True,
      buttons=[("Save", True), ("Cancel", False)],
    )
    # If the alert returned 'True', the save button was clicked.

    if save_clicked:
        anvil.server.call('add_stacked_chart',new_stacked_chart )
    pass
  
  #Sparklines
  def button_29_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_2.visible = True
    self.plot_2.figure = anvil.server.call('get_sparklines')
    pass
  
  #Sparkline Facets
  def button_30_click(self, **event_args):
    """This method is called when the button is clicked"""
#     self.plot_5.visible = True
#     self.plot_5.figure = anvil.server.call('get_sparklines_facets')
    pass

  def chart_plot_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_2.visible = True
    self.plot_2.figure = anvil.server.call('get_chart')
    pass
   # get api chart data
  def button_25_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('get_api_call')
    
    pass

  def button_31_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_email',"sydney.w.stewart@gmail.com")
    pass
  # sales sparklines
  def button_32_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_2.visible = True
    fig = anvil.server.call('get_sparklines_sales')
    self.plot_2.figure = fig
    pass

  def button_33_click(self, **event_args):
    """This method is called when the button is clicked"""
#     open_form('Form2')
    anvil.server.call('send_pdf_email_sales')
    pass 

  def button_34_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email_support')
    pass

  def button_35_click(self, **event_args):
    """This method is called when the button is clicked"""
#     open_form('support_sparklines')
    self.plot_2.visible= True
    fig = anvil.server.call('get_sparklines_support')
    self.plot_2.figure = fig
    pass

  def button_36_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email_support_sparks')
    pass

  def button_37_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Form3')
#     for x in cases:
#       print(x['Date_Entered'])
    pass

  def button_39_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    EXCHR ="GBPCAD=X"
    anvil.server.call('get_usgb', Globals.offset, EXCHR)
    pass

  def button_38_click(self, **event_args):
    """This method is called when the button is clicked"""
    from . import Globals
    EXCHR ="GBPEUR=X"
    anvil.server.call('get_usgb', Globals.offset, EXCHR)
    pass

   
   #Manual Background task
  def button_40_click(self, **event_args):
    """This method is called when the button is clicked"""
    ticker ="GBPUSD=X"
    from . import Globals
    anvil.server.call('get_gb_usd_background',Globals.offset, ticker)
    pass

  def button_41_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Chart_form')
    pass

  def button_42_click(self, **event_args):
    """This method is called when the button is clicked"""
    file_contents = "Hello, world".encode()      # String as bytes

    my_media = anvil.BlobMedia(content_type="text/plain", content=file_contents, name="hello.txt")

    anvil.google.drive.app_files.my_file.set_media(my_media)
    pass









 







 





















 


















