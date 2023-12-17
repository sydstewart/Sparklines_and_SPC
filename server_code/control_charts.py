import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import anvil.mpl_util
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import io

@anvil.server.callable  
def control_charts():
        # Set random seed
        np.random.seed(42)
        
        # Create dummy data
        x = pd.Series(np.random.normal(loc=10, scale=2, size=10))
        print(x)
        
        chartid = 57
        dfcsv = anvil.server.call('ols_data',chartid)
        print('dfcsv count=', len(dfcsv))
        # Define list variable for moving ranges
        MR = [np.nan]
        
        # Get and append moving ranges
        i = 1
        for data in range(1, len(x)):
            MR.append(abs(x[i] - x[i-1]))
            i += 1
        
        # Convert list to pandas Series objects    
        MR = pd.Series(MR)
#         dfcsv['range'] = MR
        
        # Concatenate mR Series with and rename columns
        data = pd.concat([x,MR], axis=1).rename(columns={0:"x", 1:"mR"})
        
        # Plot x and mR charts
        fig, axs = plt.subplots(2, figsize=(15,15), sharex=True)
        
        # x chart
        axs[0].plot(data['x'], linestyle='-', marker='o', color='black')
        axs[0].axhline(statistics.mean(data['x']), color='blue')
        axs[0].axhline(statistics.mean(data['x'])+3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128, color = 'red', linestyle = 'dashed')
        axs[0].axhline(statistics.mean(data['x'])-3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128, color = 'red', linestyle = 'dashed')
        axs[0].set_title('Individual Chart')
        axs[0].set(xlabel='Unit', ylabel='Value')
        
        # mR chart
        axs[1].plot(data['mR'], linestyle='-', marker='o', color='black')
        axs[1].axhline(statistics.mean(data['mR'][1:len(data['mR'])]), color='blue')
        axs[1].axhline(statistics.mean(data['mR'][1:len(data['mR'])])+3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525, color='red', linestyle ='dashed')
        axs[1].axhline(statistics.mean(data['mR'][1:len(data['mR'])])-3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525, color='red', linestyle ='dashed')
        axs[1].set_ylim(bottom=0)
        axs[1].set_title('mR Chart')
        axs[1].set(xlabel='Unit', ylabel='Range')
        
        # Validate points out of control limits for x chart
        i = 0
        control = True
        for unit in data['x']:
            if unit > statistics.mean(data['x'])+3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128 or unit < statistics.mean(data['x'])-3*statistics.mean(data['mR'][1:len(data['mR'])])/1.128:
                print('Unit', i, 'out of cotrol limits!')
                control = False
            i += 1
        if control == True:
            print('All points within control limits.')
            
        # Validate points out of control limits for mR chart
        i = 0
        control = True
        for unit in data['mR']:
            if unit > statistics.mean(data['mR'][1:len(data['mR'])])+3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525 or unit < statistics.mean(data['mR'][1:len(data['mR'])])-3*statistics.mean(data['mR'][1:len(data['mR'])])*0.8525:
                print('Unit', i, 'out of control limits!')
                control = False
            i += 1
        if control == True:
            print('All points within control limits.')
        return anvil.mpl_util.plot_image()

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
    noteCol =t['noteCol']

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
        end_date = end_date.strftime("%Y-%m-%d ")
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
  

@anvil.server.callable  
def get_pdcalls_range(chartid):
    import pandas as pd
    import anvil.server
    from tables import app_tables
        # Import Plotly and our data
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots


    dfcsv, nameCol, dateCol, title, conf_limit, formatCol, noteCol = ols_data(chartid)
#     print('dfcsv count=', len(dfcsv))
#     start_date = '30/08/2020'
#     end_date = '30/03/2021'
#     dfcsv = dfcsv.loc[(dfcsv[dateCol] >= start_date) & (dfcsv[dateCol] <= end_date)]
    
#   print('dfcsv count=', len(dfcsv))
  
    #Make X and Mr charts
    fig = make_subplots(rows=2, cols=1 , row_heights=[0.5, 0.5], subplot_titles = ("Individual Chart","Range Chart"))
   
    #Plot points 
    fig.add_trace(
      go.Scatter(x=dfcsv[dateCol],
                              y= dfcsv[nameCol],
    
                            mode='markers+lines',
                              name='All Points',
                              visible = True,
                              line=dict(color='black', width=1)),
      row=1, col=1)
    
    # Calculate Mean of points
    dfcsv['mean'] = dfcsv[nameCol].mean()
     
    pointmean = dfcsv['mean']
    print('pointmean=', pointmean)
    
    #Plot mean line of points
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                          y=dfcsv['mean'],
                          mode='lines',
                          name='Mean of Points',
                          line=dict(
        color=('green'),
        width=2,
        dash='dash'),
        visible=True),
        row=1, col=1)
      
     # Count rows in dataframe
    count_row = dfcsv.shape[0]
    
    # Get and append moving ranges
    # create the ranges
    dsd = pd.DataFrame({'Range': []})
    firstentry = dfcsv[nameCol].first_valid_index()
#     print('First entry=', firstentry)
    for k in range(1, count_row):

        dr = (dfcsv[nameCol].iloc[k] - dfcsv[nameCol].iloc[k-1])
        dr = abs(dr)
        dsd = dsd.append({'Range': dr}, ignore_index=True)
    dsd['Range'] = dsd['Range']
    print('dsd range=',dsd['Range'])
    dfcsv['Range'] = dsd['Range']
    print('Range', dfcsv['Range'])
    dfcsv['Range'] = dfcsv['Range'].shift(1)
    dfcsv['Range'] = ABS(dfcsv['Range'])
    rangemean  = dsd['Range'].mean()  
    dfcsv['rangemean'] = rangemean 
#     print('rangemean=',dfcsv['rangemean'])
    
    #Plot LCL of points
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                        y=(pointmean - (dfcsv['rangemean'] * 3)/ 1.128),
                        mode='lines',
                        name='LCL',
                        line=dict(
        color=('red'),
        width=1,
        dash='dash'),
        visible=True),
        row=1, col=1)
    
    #Plot UCL of points
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                    y=(pointmean + (dfcsv['rangemean'] * 3)/ 1.128),
                    mode='lines',
                    name='UCL',
                    line=dict(
    color=('red'),
    width=1,
    dash='dash'),
    visible=True

    ),row=1, col=1)

       
    # plot ranges
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                    y=(dsd['Range']),
                    mode= 'markers+lines',
                    name='Range',
                    line=dict(
    color=('black'),
    width=1
    ),
    visible=True

    ),row=2, col=1)
    
    # plot range mean
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                    y=(dfcsv['rangemean']),
                    mode= 'lines',
                    name='Range Mean',
                    line=dict(
    color=('green'),
    width=1
    ),
    visible=True

    ),row=2, col=1)

    # plot UCL range
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                    y=(rangemean + (dfcsv['rangemean'] * 0.8525)),
                    mode= 'lines',
                    name='UCL Range',
                    line=dict(
    color=('red'),
    width=1, dash='dash'
    ),
    visible=True

    ),row=2, col=1)
    
    # plot LCL range
    fig.add_trace(go.Scatter(x=dfcsv[dateCol],
                    y=(rangemean - (dfcsv['rangemean'] * 0.8525)),
                    mode= 'lines',
                    name='LCL Range',
                    line=dict(
    color=('red'),
    width=1, dash='dash'
    ),
    visible=True

    ),row=2, col=1)
    
  

    fig.update_xaxes(tickangle= 45)
    fig.update_layout(plot_bgcolor ="white")
    fig.update_layout(height=1600, width=800, title_text=title + " X and mR plots")
    return fig
    
  
  
@anvil.server.callable  
def control_charts_plotly():
        # Set random seed
#         np.random.seed(42)
        
#         # Create dummy data
#         x = pd.Series(np.random.normal(loc=10, scale=2, size=10))
#         print(x)
        
        chartid = 79
        dfcsv  , nameCol, dateCol, title, conf_limit, format_col = anvil.server.call('ols_data',chartid)
        print('dfcsv count=', len(dfcsv))
#         df['WeekDate'] =  pd.to_datetime(df['WeekDate'], format= '%d/%m/%Y') 
#         print(dfcsv)
#         print(df['Date_entered'])
#         df = df[0:len(df)]
#         x = df['No. of Arriving Calls'].tolist()
#         d = df['WeekDate'].tolist()
#         df['mean'] = df['No. of Arriving Calls'].mean()
#         df['SD'] = df['No. of Arriving Calls'].std()
        
#         m = df['mean'].tolist()
#         df['upper_limit']= (df['SD'] * 3) + df['mean']
#         df['lower_limit']= df['mean'] - (df['SD']*3)  
#         ul = df['upper_limit'].tolist()
#         ll = df['lower_limit'].tolist()
#         print('ll=', ll)
#         MR = [np.nan]
        
#         # Get and append moving ranges
#         i = 1
#         for data in range(1, len(x)):
#             MR.append(abs(x[i] - x[i-1]))
#             i += 1
#         print('MR=', MR)
#         print('x=',x)
        
#         #Convert list to pandas Series objects    
#         MR = pd.Series(MR)
#         x  = pd.Series(x)
#         d  = pd.Series(d)
        
#         data = pd.concat([d, x, MR], axis=1).rename(columns={0:"d", 1:"x", 2:"mR"})
#         # # data = pd.concat([d, x, MR, ul, ll], axis=1).rename(columns={0:"d", 1:"x", 2:"mR",3:"ul",4:"ll"})
#         # data =data[100:174]
#         data['rangemean'] = data['mR'].mean()
#         data['SD'] = data['mR'].std()
#         rm = data['rangemean'].tolist()
#         data['rucl']= (data['SD'] * 3) + data['rangemean']
#         rucl = data['rucl'].tolist()
        
#         data['rlcl']=  data['rangemean'] - (data['SD'] * 3) 
#         rlcl = data['rlcl'].tolist()
#         # if rlcl[0] < 0:
#         #   rlcl = 0
#         # print( rangemean)
       
        scatter = [go.Scatter(x=dfcsv[dateCol],
                              y= dfcsv[nameCol],
    
                            mode='markers+lines',
                              name='All Points',
                              visible = True,
    #                           yaxis ='y0',
    #                           yxis0  = dict(title='No. of Arriving Calls',overlaying='y',side='left'),
                              line=dict(color='firebrick', width=1)),
      #                          line=dict(color='#2196f3')),
                  ]
        
        return scatter
#         fig = make_subplots(rows=2, cols=1, subplot_titles=("Individual Chart", "Range Chart"))
        
#         fig.append_trace(go.Scatter(
#             x=dfcsv[dateCol],
#             y=dfcsv[nameCol],
#             name = 'Points',
#             line=dict(color='black', width=1),
#             mode='lines+markers'
#         ), row=1, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=m,
#             name = 'Mean',
#             line=dict(color='royalblue', width=2)
#         ), row=1, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=ul,
#             name = 'Upper control Limit',
#             line=dict(color='red', width=1, dash='dash')
#         ), row=1, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=ll,
#             name = 'Lower control Limit',
#             line=dict(color='red', width=1, dash='dash')
#         ), row=1, col=1)
        
        
#         #
#         #
#         #
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=MR,
#             name = 'Ranges',
#             line=dict(color='black', width=1),
#             mode='lines+markers'
#         ), row=2, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=rm,
#             name = 'Range Mean',
#             line=dict(color='royalblue', width=1),
            
#         ), row=2, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=rucl,
#             name = 'Range Upper control Limit',
#             line=dict(color='red', width=1, dash='dash')
#         ), row=2, col=1)
        
#         fig.append_trace(go.Scatter(
#             x=d,
#             y=rlcl,
#             name = 'Range Lower control Limit',
#             line=dict(color='red', width=1, dash='dash')
#         ), row=2, col=1)
        
        fig.update_layout(height=700, width=1500, title_text="No of Cases Arriving",plot_bgcolor = '#fff')
        return fig
        
        