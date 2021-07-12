import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from . import Globals



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