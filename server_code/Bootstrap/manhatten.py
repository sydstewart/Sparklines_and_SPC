import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import io
from .firstcusum import firstcusum
from .cusbootstrap import cusbootstrap
from .get_boot_num import get_boot_num
from .stagemeans import stagemeans
 

@anvil.server.callable
def manhatten(df, name_col, date_col, title, turn_length, boot_num, conf_limit, chartid, format_col):
    import pandas as pd
#     from . manhatten import manhatten 
#     from .firstcusum import firstcusum
#     from .cusbootstrap import cusbootstrap
#     from .stagemeans import stagemeans

    import plotly.graph_objects as go
  
    df = pd.DataFrame(df) 
    print('df from manhatten', df)
#     print(f"Preparing Cusums for {title}")
#     print('-'*100)
#     print('-'*100)
#     print()

    # count rows in dataframe - note 1 is subtrated as the first index in a  list is set to 0
    total_rows = df[name_col].count() - 1

#     print('Find Turning points in Cusum')
#     print('-'*100)
#     print('-'*100)
#     print()

    # setup dataframe to hold cusum turning points
    cusum_control = pd.DataFrame(columns=['firstindex', 'firstdate', 'lastindex',
                                          'lastdate', 'conflevel', 'changeptindex', 'StageMean', 'Expanded'])

    # print(' Finding and setting the first and last indices in the series of points')
    # print('-'*100)
    # print('-'*100)
    # print()

    firstindex = 0
    lastindex = int(total_rows)

#     print('Creating the first row in a cusum dataframe using the first and last indices in the series of points')
#     print('-'*100)
#     print('-'*100)
#     print()

    cusum_control = cusum_control.append(
        {'firstindex': firstindex, 'lastindex': lastindex}, ignore_index=True)


    countr = 0  # count of rows in cusun_control
    fog = [0]  # initialise List

    fogstart = datetime.now()
    for x in fog:
#       x is the no of steps or stages


        # note a 'cusum stage' is the points that lie between two turning points in the cusum
        # the index is the sequential number in the cusum panda dataframe
        # z is the starting index of the cusum stage
        # y is the final index of the cusum stage
        # x is the row or stage number of the cusum stage

        then = datetime.now()
        sdiff, dx, pointmean, turnpt, z, y = firstcusum(
            df, name_col, date_col, cusum_control, x)

        if x == 0:
            dcx = dx

 
        if (y - z) > turn_length:
#             print('0cusbootstrap) '+str(datetime.now()))
            then = datetime.now()
            conflevel, cusum_control, x, fog, countr = cusbootstrap(
                dx, pointmean, name_col, sdiff, boot_num, total_rows, cusum_control, x, fog, turnpt, z, y, countr, conf_limit)

        if x == 15:
#             print('Break at No of stage found = 15')
            break

    then = datetime.now()
    cusum_control1, manhatten = stagemeans(
        cusum_control, dx, df, name_col, date_col, format_col)
    print("StageMeans  Time: " + str(datetime.now() - then) + '\n')
  
    manpointlist = list(manhatten[date_col])
    manstagemeanlist = list(manhatten['StageMean'])
    no_of_steps = len(cusum_control1) 
    manconnfleveltextlist = list(manhatten['confleveltext'])
#     print('dcx=',dcx)
#     print('manpointlist=',manpointlist)
#     print('manstagemeanlist=',manstagemeanlist)
    dcx = dcx.to_dict(orient="records")
    
    df['mean'] = df[name_col].mean()
    df['meandiff'] = df[name_col] - df['mean']
    df['cusum']=df['meandiff'].cumsum()
    df=df.round(3)

    #store df into a csv
    filename = '/tmp/'+ str(chartid) +'.csv'
    
    df_as_csv = df.to_csv(index=False)

    csv_bytes = bytes(df_as_csv, 'utf-8') # fix

    csv_media = anvil.BlobMedia('text/plain', csv_bytes, name=filename)
    
        
#     file_row = app_tables.charts.get(id = chartid)
#     if file_row != None:
#       file_row['manhatten_csv'] = csv_media
#       #       file_row["last_uploaded"] = datetime.now()
#       alert('Manhatten File updated')
#     else:
#       alert('File does not exist - adding new file')
#       app_tables.charts.add_row(manhatten_csv=csv_media, media_obj=file) #last_uploaded = datetime.now())
      
#       file_row = app_tables.charts.get(id = chartid)
 

        
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

#     print('manconf=',manconf)
#     print("Ends creating  manconf:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
    return manconf, no_of_steps 
#   dcx, manpointlist, manstagemeanlist, manconnfleveltextlist


@anvil.server.callable
def manhatten_background(df, name_col, date_col, title, turn_length, boot_num, conf_limit, chartid, format_col):
    import pandas as pd
    from . manhatten import manhatten 
    from .firstcusum import firstcusum
    from .cusbootstrap import cusbootstrap
    from .stagemeans import stagemeans
    import plotly.graph_objects as go

    df = pd.DataFrame(df) 
    
#     print(f"Preparing Cusums for {title}")
#     print('-'*100)
#     print('-'*100)
#     print()

    # count rows in dataframe - note 1 is subtrated as the first index in a  list is set to 0
    total_rows = df[name_col].count() - 1

#     print('Find Turning points in Cusum')
#     print('-'*100)
#     print('-'*100)
#     print()

    # setup dataframe to hold cusum turning points
    cusum_control = pd.DataFrame(columns=['firstindex', 'firstdate', 'lastindex',
                                          'lastdate', 'conflevel', 'changeptindex', 'StageMean', 'Expanded'])

    # print(' Finding and setting the first and last indices in the series of points')
    # print('-'*100)
    # print('-'*100)
    # print()

    firstindex = 0
    lastindex = int(total_rows)

#     print('Creating the first row in a cusum dataframe using the first and last indices in the series of points')
#     print('-'*100)
#     print('-'*100)
#     print()

    cusum_control = cusum_control.append(
        {'firstindex': firstindex, 'lastindex': lastindex}, ignore_index=True)


    print("Start finding stages:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
    countr = 0  # count of rows in cusun_control
    fog = [0]  # initialise List

    for x in fog:
#       x is the no of steps or stages


       
        sdiff, dx, pointmean, turnpt, z, y = firstcusum(
            df, name_col, date_col, cusum_control, x)
#         print("Start finding firstcusum:", datetime.now().strftime('%d %B %Y %H:%M:%S') )

#         print('Cusum Rowx=', x)
        if x == 0:
            dcx = dx

        # print('sdiff=',sdiff)
        # print('dx',dx)
        #print( 'Running Bootstrap to Test significant turning points- 1000 bootstraps')
        #boot_num = 1000

        if (y - z) > turn_length:
            conflevel, cusum_control, x, fog, countr = cusbootstrap(
                dx, pointmean, name_col, sdiff, boot_num, total_rows, cusum_control, x, fog, turnpt, z, y, countr, conf_limit)
#             print("Start finding custbootstrap:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
    #             print('cusum_contol')
#             print(cusum_control)
#         if (y - z) <= turn_length:
#             print('Will only check for significance if there are more than',
#                   turn_length, ' in stage being examined i.e. (y-x) < ', turn_length)
#             print('First index (z)=', z, 'and Last index (y)=', y)
        # if  y == z:
        #       print(' No rows in stage')
        #       print('First index (z)=',z ,'and Last index (y)=',y)
#     print('')
#     print('Cusum_Control without dates but indices')
#     print(cusum_control)

        if x == 15:
#             print('Break at No of stage found = 15')
            break
#     print("Starts finding stages:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
#     format_col = 0
    # workout stagemeans creates a new dictionary cusum_control1
    cusum_control1, manhatten = stagemeans(
        cusum_control, dx, df, name_col, date_col, format_col)
#     print("cusum_control1")
#     print(cusum_control1)
    #plot in plotly

#     custable = go.Table(
#         header=dict(values=('StartDate', 'EndDate', 'StageMean', 'Conf. Level'),
#                     fill=dict(color='#C2D4FF'),
#                     align=['center'] * 5),
#         visible=False,
#         cells=dict(values=[cusum_control1.firstdate, cusum_control1.lastdate, cusum_control1.StageMean,
#                            cusum_control1.conflevel],
#                    fill=dict(color='#F5F8FF'),
#                    align=['center'] * 5)
#     )
    # fig = go.Figure(data=[go.Table(header=dict(values= ('StartDate', 'EndDate', 'StageMean', 'Conf. Level')),
    #                         fill = dict(color='#C2D4FF'),
    #                         align = ['center'] * 5,
    #                         visible = False,
    #                         cells=dict(values=[cusum_control1.firstdate, cusum_control1.lastdate, cusum_control1.StageMean, cusum_control1.conflevel])
    #
    #                         )])
    # # fig.show()
    # # # data = [custable]
    # # # layout = dict(title = title + ' Cusum Table')
    # # # fig = dict(data=data, layout=layout)
    # # #
    #py.plot(fig, file_name= folder_name + '/' + 'Cusum Table', sharing ='secret' )

#     dcline = go.Scatter(x=dcx[date_col],
#                         y=dcx['Cusum'],
#                         mode='markers+lines',
#                         name='Cusum',
#                         visible=False,
#                         marker=dict(
#                         color='blue',
#                         size=2,
#                         line=dict(
#                                         color='brown',
#                                         width=2)
#     )
#     )
#     print("Ends finding stages:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
#     print("Starts creating  manconf:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
    manpointlist = list(manhatten[date_col])
    manstagemeanlist = list(manhatten['StageMean'])
    no_of_steps = len(cusum_control1)
    manconnfleveltextlist = list(manhatten['confleveltext'])
#     print('dcx=',dcx)
#     print('manpointlist=',manpointlist)
#     print('manstagemeanlist=',manstagemeanlist)
    dcx = dcx.to_dict(orient="records")
    
    df['mean'] = df[name_col].mean()
    df['meandiff'] = df[name_col] - df['mean']
    df['cusum']=df['meandiff'].cumsum()
    df=df.round(3)

        
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

#     print('manconf=',manconf)
#     print("Ends creating  manconf:", datetime.now().strftime('%d %B %Y %H:%M:%S') )
    return manconf, no_of_steps 
