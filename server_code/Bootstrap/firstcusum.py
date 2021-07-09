import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def firstcusum(df, pointname, pointdate, cusum_control, x):
    import pandas as pd
#     print('Syd99', pointname, pointdate, cusum_control, x)
#     print('-------------------------------------------')
#     print('firstcusum')
#     print('-------------------------------------------')
    # Create the cusum and finds the max diff in cusum values
    dx = pd.DataFrame(columns=[pointdate, pointname, 'Mean', 'Diff from mean', 'Cusum', 'shuffle', 'ShuffCusum'])

    pd.options.display.float_format = '{:.2f}'.format

    # print(dx)
#     print('')
#     print('')
#     print('')
#     print('-------------------------------------------')
#     print('Seek new turnpt for the stage or row in cusum_control =', x)
#     print('-------------------------------------------')

#     print('-------------------------------------------')
#     print('Turning Pts finding for row ', x, 'creating row =', 1 + (x)*2, ' and row =', 2 + (x)*2)
#     print('-------------------------------------------')

   # from Cusum_control find the first and last indices  of the stage being examined
   # X is the row or stage number starting at zero. The following logic works on the
   # basis the next stage is the turning point plus 1 so the stages do not overlap
#     print('0Afirstcusum) '+str(datetime.now()))
    if x <= 1:
        z = int((cusum_control['firstindex'].iloc[x]))
#         print('z=', z)

        y = int(cusum_control['lastindex'].iloc[x])
#         print('y=', y)

    if x >= 2:
        z = int((cusum_control['firstindex'].iloc[x])) + 1
#         print('z=', z)

        y = int(cusum_control['lastindex'].iloc[x])
#         print('y=', y)
    then = datetime.now()
    # create a new dataframe for the subset of df between the start and end indices
#     for k in range(z, y + 1):

#         dx = dx.append({pointdate: df[pointdate].iloc[k], pointname: df[pointname].iloc[k]},
#                        ignore_index=True)
#     print(" Build dx Time: " + str(datetime.now() - then) + '\n')
#     # reindex dx

#     dx.index = pd.RangeIndex(start=z, stop=y + 1, step=1)
    dx = df.iloc[z:y]
    # Calculate Mean and Cusum table vulues

    dx['Mean'] = dx[pointname].mean()

    pointmean = dx[pointname].mean()

    dx['Diff from mean'] = dx[pointname] - pointmean

    dx['Cusum'] = dx['Diff from mean'].cumsum()

#     print('-------------------------------------------')
#     print('-------------------------------------------')
#     print('Table of Mean and Cusum')
#     print(dx)
#     print('-------------------------------------------')
#     # Find the cusum diff
#     print('Maximum and Minimum cusum')
    maxcusum = dx['Cusum'].max()
#     print('MaxCusum=', maxcusum)
    mincusum = dx['Cusum'].min()
#     print('MinCusum=', mincusum)
#     print('Rows in dx=', dx['Cusum'].count())

    # Find turning point depending on whet=her the maxcusum is greater or less than the Minimum

    sdiff = maxcusum - mincusum
#     print('Sdiff=', sdiff)
    # find index value of turning point
    # turnpt = int(dx['Cusum'].idxmax()))
    # print ('Turnptmin=',turnpt)
    stagemean = dx[pointname].mean()
#     print('Stagemean=', stagemean)

    # if (maxcusum) <  (mincusum):
    #     sdiff = mincusum - maxcusum
    #     #find index value of turning point
    #     turnpt = int(dx['Cusum'].idxmin()))
    #     print ('Sdiff=',sdiff)
    #     print ('Turnptmax1=',turnpt)
    #     stagemean =dx[pointname].mean()
    #     print ('Stagemean=',stagemean)
    turnpt = 0
    # sets positive or negative turning pts and works out where the turning pt is
#     print('1Afirstcusum) '+str(datetime.now()))
#     print('abs(maxcusum) & abs(mincusum',abs(maxcusum),abs(mincusum))
    if  dx['Cusum'].isnull().values.any():
          print('dx([Cusum] is empty)')
    if abs(maxcusum) > abs(mincusum):  # sets idmax or idmin
          #sdiff = maxcusum - mincusum
        turnpt = dx['Cusum'].idxmax()
#         print('Turnptmax when maxcusum > 0 and mincusum < 0 =', turnpt)

    # if abs(maxcusum) > abs(mincusum):
    #       #sdiff = maxcusum - mincusum
    #           turnpt =  dx['Cusum'].idxmax()
    #           print ('Turnptmax when maxcusum > 0 and mincusum > 0 =',turnpt)

    if abs(maxcusum) <= abs(mincusum):
          #sdiff = maxcusum - mincusum
        turnpt = dx['Cusum'].idxmin()
#         print('Turnptmin when maxcusum < 0 and mincusum > 0 =', turnpt)
#     print('turnpt=',turnpt)
    return sdiff, dx, pointmean, turnpt, z, y

