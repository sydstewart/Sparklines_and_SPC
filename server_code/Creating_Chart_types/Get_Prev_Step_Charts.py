import anvil.email
import tables
from tables import app_tables
import anvil.server
import io
import plotly.graph_objects as go
import datetime as dt
import json
from datetime import datetime
import anvil.tables.query as q
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime , timedelta
import plotly

import anvil.media 
import anvil.email


# @anvil.email.handle_message
# def handle_incoming_emails(msg):
  
#   msg.reply(text="Thank you for your message.")

#   msg_row = app_tables.received_messages.add_row(
#               from_addr=msg.envelope.from_address, 
#               to=msg.envelope.recipient,
#               text=msg.text, 
#               html=msg.html
#             )
#   for a in msg.attachments:
#     app_tables.attachments.add_row(
#       message=msg_row, 
#       attachment=a
#     )

# @anvil.email.handle_message()
# def message_handler(msg):
#   print("Message received from %s" % msg.addressees.from_address.raw_value)

#   msg.reply(text="Thanks for your email - received OK!")


 

@anvil.server.callable
def get_conf_limits(chartid):
    # some way to get it from the data table. obviously change as needed
     t = app_tables.charts.get(id= chartid)
     conf_limit_text = t['conf_limit_text']
     last_conf_limit = t['last_conf_limit']
     return conf_limit_text,last_conf_limit
    
@anvil.server.callable
def list_charts_not_archived():
    # some way to get it from the data table. obviously change as needed
    charts = app_tables.charts.search(q.any_of(archive = False, file_name = None))
  
    return charts    

    
@anvil.server.callable
def list_charts(chartid):
    # some way to get it from the data table. obviously change as needed
     charts = app_tables.charts.search(file_name= q.not_(None), id =chartid)
   
     return charts
  
@anvil.server.callable
def list_charts_chart_date_greater_than_file_date():
    # some way to get it from the data table. obviously change as needed
     charts = app_tables.charts.search(file_name= q.not_(None))
     result = []
  
     for row in charts:
       if row['file_name'] != None and row['Chart_last_saved'] != None: 
              if row['Chart_last_saved'] < row['file_name']['last_uploaded']:
                  result.append(row)
        
     return result

@anvil.server.callable
def list_charts_chart_date_less_than_file_date():
    # some way to get it from the data table. obviously change as needed
     charts = app_tables.charts.search(file_name= q.not_(None))
     result = []
  
     for row in charts:
       if row['file_name'] != None and row['Chart_last_saved'] != None: 
              if row['Chart_last_saved'] > row['file_name']['last_uploaded']:
                  result.append(row)
        
     return result




@anvil.server.callable
def list_charts_by_folder (foldername):
#      folder_title =foldername['Folder']['folder_name']
#      print(folder_title)
    # some way to get it from the data table. obviously change as needed
     charts = app_tables.charts.search(folder_name = foldername)
   
     return charts





@anvil.server.callable
def get_no_of_steps(chartid):
    tcharts = app_tables.charts.get(id = chartid)
    no_of_steps = tcharts['no_of_steps']
    return no_of_steps

@anvil.server.callable
def get_csvdatetime_loaded(chartid):
    tcharts = app_tables.charts.get(id = chartid)
    csvfilename = tcharts['file_name']['name']
    print('csvfilename=',csvfilename)
    tfiles = app_tables.my_files.get(name = csvfilename)
    csvdatetime = tfiles['last_uploaded']  
    print('csvdatetime=',csvdatetime)
    return csvdatetime

@anvil.server.callable
def get_Chart_last_saved(chartid):
    tcharts = app_tables.charts.get(id = chartid)
    Chart_last_saved = tcharts['Chart_last_saved']
#     json = tcharts['json']
#     print('json=',json)
#     if json == '':
#         tcharts['Chart_last_saved'] = datetime.now()
#     print('Updated Chart_last_saved to=',Chart_last_saved)
    return Chart_last_saved 
  

 
@anvil.server.callable
def send_email(address , chartid):
    t = app_tables.charts.get(id= chartid)
    picture =t['Chart_image']
    
    
    anvil.email.send(
      from_name="Anvil Forum",
      subject="Have you used the Anvil Forum?",
#       html='The Anvil <a href="https://anvil.works/forum">Forum</a> is friendly and informative.',
#       text="The Anvil Forum (https://anvil.works/forum) is friendly and informative.",
      html=""" Here's a picture:<br> <img src="cid:mypic"><br> Wasn't that cute? """,
      inline_attachments={'mypic': picture}
      
    )


  



@anvil.server.callable
def get_contents(phrase, archive):
  """Extra example: full log search widget."""
#   a = app_tables.charts.search(q.any_of(
#     title=q.full_text_match(phrase),folder_name = (phrase)))
  my_list = [phrase]
  app_tables.charts.search(folder=q.any_of(*my_list), archive = archive)
#   a = app_tables.charts.search(folder =q.any_of(*[phrase]))
  return a 


@anvil.server.callable
def get_shared_users(chart_id):
  current_user = anvil.users.get_user()
#   shared_rows = list(dict(r) for r in app_tables.chart_shares.search(chart_id = chart_id))
#   selected_user_row = app_tables.users.get(email = chart_owner)
  shared_rows = app_tables.folder_shares.search(FolderUser = current_user)
  return shared_rows
  


  
  

   
 



  
 
  

  
@anvil.server.callable
def user_type_status():
  current_user = anvil.users.get_user()
  user_type = current_user['user_type']
  print(current_user['user_type'])
  
  return user_type
  
      

  
  
@anvil.server.callable
def update_chart(chart, chart_dict):
  # check that the article given is really a row in the ‘articles’ table
  if app_tables.charts.has_row(chart):
   chart_dict['updated_last'] = datetime.now()
   chart.update(**chart_dict)
  else:
    raise Exception("Chart does not exist")
    

    
  

@anvil.server.callable
def update_folders(folders, folder_copy):
  # check that the article given is really a row in the ‘articles’ table
  if app_tables.folders.has_row(folders):
#     article_dict['updated'] = datetime.now()
    Creator = anvil.users.get_user()
    folders.update(**folder_copy)
  else:
    raise Exception("Folder does not exist")
    
@anvil.server.callable
def delete_folders(folder_name):
      folder_row = app_tables.folders.get(folder_name=folder_name)
      if folder_row is not None:
          folder_row.delete() 
  
 
  
@anvil.server.callable
def store_data(file):
  with anvil.media.TempFile(file) as file_name:
#     if file.content_type == 'text/csv':
      df = pd.read_csv(file_name)
#     else:
#       df = pd.read_excel(file_name)
      for d in df.to_dict(orient="records"):
        # d is now a dict of {columnname -> value} for this row
        # We use Python's **kwargs syntax to pass the whole dict as
        # keyword arguments
        app_tables.upgrades.add_row(**d)

@anvil.server.callable
def get_charts(foldername):
  folder = app_tables.folders.get ( folder_name= foldername)
  folder_charts = app_tables.charts.search(folderid =folder)
  print(f"There are {len(folder_charts)} charts.")
#    chartids = t['title']
#    print(chartids)
#    for row in chartids:
#       print(row)
#   charts = [(foldername['folder_name']) for foldername in app_tables.folders.search()]
#   self.folder_drop_down.items = folders_charts
  return folder_charts
        
        
        
@anvil.server.callable
def get_chart_settings(chart_title):        
    print(chart_title)  
    t = app_tables.charts.get(title=chart_title)
    nameCol = t['nameCol']
    dateCol = t['dateCol']
    title =  t['title']
    fileName =t['fileName']
    id=t['id']
    start_date =t['start_date']
    end_date =t['end_date']
    conf_limit =t['confLimit']
    conf_limit_text = t['conf_limit_text']
    moving_avg =t['mov_avg']

    print('start_date=',start_date)
    return start_date , end_date, conf_limit_text, moving_avg
  
@anvil.server.callable
def update_chart_settings(chart_title, conf_limit_text, start_date, end_date , moving_avg):        
    print(chart_title)
    print('From Update module',conf_limit_text)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    t = app_tables.charts.get(title=chart_title)
    t.update(title=chart_title, startDate = start_date,endDate = end_date, conf_limit_text = conf_limit_text, mov_avg = moving_avg \
            )
#     t.update(conf_limit_text = conf_limit_text,)
#     t.update(conf_limit_text = conf_limit_text )
#     start_date = start_date.strftime("%Y-%m-%d")
#     t.update(startDate = start_date )
#     end_date = end_date.strftime("%Y-%m-%d")
#     t.update(endDate = end_date )
#     print(start_date)p
    
    pass
  
# start_date, end_date, conf_limit        
#CUSUM
@anvil.server.callable
def get_pdcalls_cusum(chartid):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    dfcsv, nameCol, dateCol, title , conf_limit, formatCol = ols_data(chartid)

    signups = dfcsv
    turn_length = 5
    boot_num = 1000
    conf_limit = 95
    
    scatter = [ go.Scatter(x=dfcsv[dateCol],
                           y= dfcsv[nameCol],
#                          fill='tozeroy',
                         mode='markers+lines',
                          name='All Points',
#                           visible = True,
#                           yaxis ='y1',
#                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                          line=dict(color='firebrick', width=1)),
#                            line=dict(color='#2196f3')),
                go.Scatter(x= dfcsv[dateCol],
                           y = dfcsv['cusum'],
                           name="Cusum",
                           line=dict(color='green', width=2),
                           yaxis="y2"),
                go.Scatter(x= dfcsv[dateCol],
                           y = dfcsv['mean'],
                           name="Time period Mean",
                           line=dict(color='blue', width=1),
#                            yaxis="y2"
                          )
                           ]
    

    return scatter
  
    


#CHECK IF CSV FILE EXISTS
@anvil.server.callable  
def check_file_exists(chart_title):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    
    t = app_tables.charts.get(title=chart_title)
    nameCol = t['nameCol']
    dateCol = t['dateCol']
    title =  t['title']
    fileName =t['fileName']
    id=t['id']
    start_date =t['startDate']
    end_date =t['endDate']
    conf_limit =t['confLimit']
    print(fileName)
    mname = app_tables.my_files.get(name=fileName)
    print(mname)
    return mname
  
  

  

@anvil.server.callable
def get_users():
  return app_tables.users.search(tables.order_by("email", ascending=True))

@anvil.server.callable
def get_logged_in_users():
  app_tables.users.search(
    last_login =q.greater_than(datetime.now() - timedelta(seconds=5))
  )
  
#   user = anvil.users.get_user()
#   for user in user:
#       print (user['email'])
#   return user

# anvil.users.get_user(tables.order_by("email", ascending=True))

@anvil.server.callable
def get_csvs():
  return app_tables.my_files.search(tables.order_by("name", ascending=True))

import anvil.server
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

@anvil.server.callable
def last_date_update_background():
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('update_chart_end_date')

  if task.is_completed():
     
     return task
  
@anvil.server.background_task
# @anvil.server.callable
def update_chart_end_date():
#   print('0) '+str(datetime.now()))
  t = app_tables.charts.search(End_date_Overwrite = False)
  for row in t:
      row['aend_date'] = datetime.now()
      print (row['aend_date'])

@anvil.server.callable
# @anvil.server.background_task
def get_chart_background():
    """Launch a single crawler background task."""
    
    task = anvil.server.launch_background_task('batch_step_charts')
    print("calling chart background generation")
    return task


 
@anvil.server.background_task
def batch_step_charts():
   
    from ..Bootstrap.get_manhatten_data import get_pdcalls_manhatten
    from ..Chart_Maintenance.Loading_Saving_Charts_JSON import save_as_json
    charts  = anvil.server.call('list_charts_not_archived') # when filename exist
    for row in charts:
                print (row['id'])
                chartid = row['id']
 
                conf_limit_text, last_conf_limit = anvil.server.call('get_conf_limits', chartid)
#                 print("crawl was run in background")
                manconf, conf_limit = get_pdcalls_manhatten(chartid)
                no_of_steps = anvil.server.call('get_no_of_steps', chartid)
                save_as_json(chartid, manconf, no_of_steps)
#                 print ( 'Json saved')
            
@anvil.server.callable
# @anvil.server.background_task
def get_chart_background_individual(chartid):
    """Launch a single crawler background task."""
    
    task = anvil.server.launch_background_task('step_chart_individual', chartid)
    print("calling chart background generation")
    return task
  
@anvil.server.background_task
def step_chart_individual(chartid):
   
    from ..Bootstrap.get_manhatten_data import get_pdcalls_manhatten
    from ..Chart_Maintenance.Loading_Saving_Charts_JSON import save_as_json

    conf_limit_text, last_conf_limit = anvil.server.call('get_conf_limits', chartid)
#                 print("crawl was run in background")
    manconf, conf_limit = get_pdcalls_manhatten(chartid)
    no_of_steps = anvil.server.call('get_no_of_steps', chartid)
    save_as_json(chartid, manconf, no_of_steps)
#                 print ( 'Json saved')     

# @anvil.server.background_task
# def get_conf_limits_background(chartid):
#     # some way to get it from the data table. obviously change as needed
#      t = app_tables.charts.get(id= chartid)
#      conf_limit_text = t['conf_limit_text']
#      last_conf_limit = t['last_conf_limit']
#      return conf_limit_text,last_conf_limit
@anvil.server.callable
def get_user_type(loggedinuser):

    t = app_tables.users.get(email = loggedinuser['email']) 
    user_type = t['user_type']
    return user_type
    
@anvil.server.callable
def load_from_manhatten(chartid):
    m=app_tables.charts.get(id = chartid)['manhatten']
    date_col = app_tables.charts.get(id = chartid)['dateCol']
    name_col = app_tables.charts.get(id = chartid)['nameCol']
    df = pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[date_col] , dayfirst=True, infer_datetime_format=True)
    
    manconf = [   go.Scatter(x=df[date_col],
                        y= df[name_col],
#                          fill='tozeroy',
                      mode='markers+lines',
                      name='All Points',
#                           visible = True,
#                           yaxis ='y0',
#                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                      line=dict(color='firebrick', width=1)),
            
            go.Scatter(x=df[date_col],
                        y= df['cusum'],
#                          fill='tozeroy',
                      mode='lines',
                      name='Cusum',
#                           visible = True,
                      yaxis ='y2',
#                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                      line=dict(color='green', width=1)),

              go.Scatter(x=manpointlist,
                    y=manstagemeanlist,
                    mode='lines+markers',
                    name='SM - Stage Mean %CL',
                    text=manconnfleveltextlist,
                    textposition='top right',
#                         visible=False,
                    # secondary_y=True,
                    marker=dict(
                        color='blue',
                        size=2,
                        line=dict(
                            color='blue',
                      width=3)))

                      ]
    
    return manconf
    
@anvil.server.callable
def make_data(**kwargs):
  fileName = "Supportcases1.csv"
  dateCol = "WeekDate"
  m=app_tables.my_files.get(name = fileName)['media_obj'] 
   #Read in data file csv
  dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol] , dayfirst=True, infer_datetime_format=True)  
#   x_arr = np.array([[1,2,3]]) #placeholder data
  X = dfcsv
  X.to_csv('/tmp/X.csv')
  X_media = anvil.media.from_file('/tmp/X.csv', 'csv', 'X')
  return X_media

