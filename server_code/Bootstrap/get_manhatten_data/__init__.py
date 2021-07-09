import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import numpy as np

from ...Creating_Chart_types.Getting_Data_for_Charts import ols_data
 


@anvil.server.callable  
def get_pdcalls_manhatten(chartid):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    import math
    # Scientific libraries
    from numpy import arange, array, ones
    from scipy import stats
    import datetime as dt
    from datetime import datetime
    import io
    
#     print('0 olsdata) '+str(datetime.now()))
    
    dfcsv, nameCol, dateCol, title , conf_limit, format_col, noteCol = ols_data(chartid)
    
#     print('1 olsdata) '+str(datetime.now()))
#     pointmean = dfcsv[nameCol].mean()

#     dfcsv['Diff from mean'] = dfcsv[nameCol] - pointmean

#     dfcsv['Cusum'] = dfcsv['Diff from mean'].cumsum()

    
#     local_min = (np.diff(np.diff(dfcsv['Cusum'])) > 0).nonzero()[0] + 1
# #     print('Cusum local_min=', local_min)
    
#     local_max = (np.diff(np.diff(dfcsv['Cusum'])) < 0).nonzero()[0] + 1
# #     print('Cusum local_max=', local_max)
    
    
#     no_of_mins = len(local_min)
# #     print('Cusum No of Mins=', no_of_mins)
    
#     no_of_maxs = len(local_max)
# #     print('Cusum No of Maxs =', no_of_maxs)
    
#     no_of_turn_pts = no_of_maxs + no_of_mins
    
#     print ('Cusum Total no. of Turning Points =',no_of_turn_pts)
    
    then = datetime.now() 
    dfcsv = dfcsv.to_dict(orient="records")
     
    turn_length = 5
    boot_num, backbootnum = anvil.server.call('get_boot_num',chartid)
    print('boot_num=',boot_num)
#     print('0 manhatten) '+str(datetime.now()))
    manconf , no_of_steps = anvil.server.call('manhatten', dfcsv, nameCol, dateCol,title, turn_length, boot_num, conf_limit,chartid, format_col)
    
#     print('1 manhatten) '+str(datetime.now()))
#     print("Calling manhatten (pd_calls_man) Time: " + str(datetime.now() - then) + '\n')

    return manconf ,  no_of_steps

  #BACKGROUND
@anvil.server.background_task
def get_pdcalls_manhatten_background(chartid):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    import math
    # Scientific libraries
    from numpy import arange, array, ones
    from scipy import stats
    import datetime as dt
    import io
#     from  ..ServerPackage2.ServerModule1 import ols_data
    from ..Creating_Chart_Types.Getting_Data_for_Charts import ols_data
    
    dfcsv, nameCol, dateCol, title , conf_limit, format_col = ols_data(chartid)
    
#     pointmean = dfcsv[nameCol].mean()

#     dfcsv['Diff from mean'] = dfcsv[nameCol] - pointmean

#     dfcsv['Cusum'] = dfcsv['Diff from mean'].cumsum()
  
    
    dfcsv = dfcsv.to_dict(orient="records")

    turn_length = 5
        
    boot_num, backbootnum = anvil.server.call('get_boot_num',chartid)

    manconf, no_of_steps = anvil.server.call('manhatten_background', dfcsv, nameCol, dateCol,title, turn_length, backbootnum, conf_limit, chartid, format_col)
    
    return manconf , no_of_steps
   
@anvil.server.callable
def launch_one_crawler(chartid):
  """Launch a single crawler background task."""
  
  manconf,conf_limit  = anvil.server.launch_background_task('get_pdcalls_manhatten',chartid)
  return manconf,conf_limit