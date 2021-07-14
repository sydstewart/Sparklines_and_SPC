import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import io


@anvil.server.callable
def ols_data(chartid):
    import pandas as pd
    import anvil.server
    from tables import app_tables
    from datetime import datetime
    then = datetime.now()
#     print('chartid=', chartid)
    t = app_tables.charts.get(id=chartid)
#     if t['file_name']['name'] is None:
#       alert(' Missing File ')
#       return
#     else:
    fileName = t['file_name']['name']

    nameCol = t['nameCol']
    dateCol = t['dateCol']
    title =  t['title']
    noteCol = t['noteCol']

    id=t['id']
    start_date =t['astart_date']
    end_date =t['aend_date']
    conf_limit =t['conf_limit_text']
    conf_limit = int(conf_limit)
    moving_avg = t['mov_avg']
#     moving_avg = int(moving_avg)
    format_col = t['formatCol']
#     print(fileName)
         
    mname = app_tables.my_files.get(name=fileName)
#     print(mname)
#     mname =app_tables.my_files.get(name = fileName)['name'] 
#     print("Start Date=",start_date)
#     print("End Date=",end_date)
    
    if mname != None:
        m=app_tables.my_files.get(name = fileName)['media_obj'] 
        t= app_tables.charts.get(id= chartid)
        dayfirst = t['DateDayFirst']
#         print('DayFirst', dayfirst)
#         dayfirst is FALSE for DD/MM  = MM/DD True
        #Read in data file csv
        dfcsv=pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol] , dayfirst=dayfirst, infer_datetime_format=True)
        dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol])
        if t['fill_missing_dates'] == True:
           freq = t['obs_interval']
           if freq == 'Month':
                freq= 'MS'
                all_dates = pd.DataFrame({dateCol:pd.date_range(start=dfcsv[dateCol].min(),
                                                    end=dfcsv[dateCol].max(),
                                                    freq=freq)})
#               elif freq == 'Week':
#                 freq= 'W'
           else:
                freq == 'Day'
                freq= 'B'
       
                all_dates = pd.DataFrame({dateCol:pd.bdate_range(start=dfcsv[dateCol].min(),
                                                    end=dfcsv[dateCol].max(),
                                                    freq=freq)})
#               if freq == 'Day':
#                 all_dates = pd.tseries.offsets.CustomBusinessDay( weekmask = 'Mon Tues Wed')
                
#            print(all_dates) 

           dfcsv = pd.merge(all_dates, dfcsv, how="left", on=dateCol).fillna(0)
    
#         date_range = pd.DataFrame({'dateCol': pd.date_range(start=dfcsv[dateCol].min(),end=dfcsv[dateCol].max(), freq='M')})
#         date_range =date_range.sort_values(date_range['dateCol'])
#         date_range = pd.DataFrame({'dateCol':set(date_range['dateCol'].dt.date)})
    
    
#         dfCombined = pd.merge(dfcsv, date_range , on="DateCol", how='outer')
#         dfCombined =dfCombined.sort_values(['DateCol'])
#         dfCombined = dfCombined.fillna(0)

#         dfcsv = dfcombined

          
#         print('dfcsv', dfcsv[dateCol])
        mindate = min(dfcsv[dateCol])
        maxdate = max(dfcsv[dateCol])
#         print('Min Date=', mindate)
#         print('Max Date=', maxdate)
        t = app_tables.charts.get(id = chartid)
#         t.update(mindate = mindate, maxdate = maxdate)
        
        start_date = start_date.strftime("%Y-%m-%d")
#         print(start_date)
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = end_date.strftime("%Y-%m-%d")
#         print(end_date)
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
      #Filter data on dates
        dfcsv = dfcsv.loc[(dfcsv[dateCol] >= start_date) & (dfcsv[dateCol] <= end_date)]
#         print("dfcsv2",dfcsv)
        No_of_Points = dfcsv.shape[0]
        print('Number of Data Points in Chart =',No_of_Points)
        dfcsv[nameCol] = dfcsv[nameCol].astype(float)
        dfcsv['mean'] = dfcsv[nameCol].mean()
        dfcsv['meandiff'] = dfcsv[nameCol] - dfcsv['mean']
        dfcsv['cusum']=dfcsv['meandiff'].cumsum()
        dfcsv=dfcsv.round(3)
#         print("Date Time =",datetime.now().strftime('%d %B %Y %H:%M') )
#         dfcsv[dateCol]= pd.to_datetime(dfcsv[dateCol])
#         print(dfcsv[dateCol])
        dfcsv['Mov_avg8'] = dfcsv[nameCol].rolling(window=moving_avg).mean()
#         print('Cusum=',dfcsv['cusum'])
#         print("Returning dfcsv")
        print("Data Load Time: " + str(datetime.now() - then) + '\n')

        return dfcsv, nameCol, dateCol, title, conf_limit, format_col, noteCol
      
