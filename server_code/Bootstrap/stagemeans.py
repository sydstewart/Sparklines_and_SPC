import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
def stagemeans (cusum_control, dx, df, pointname, pointdate, decplaces):

        import pandas as pd
        import numpy as np

        total_rowssum = cusum_control['firstindex'].count()
#         print('totrowscusum =',total_rowssum )

        final = total_rowssum
        # z =  int((cusum_control['firstindex'].iloc[0]) )
        # print (z)

        # Work out stage means from cusum control
        for x in range(0,final):

#             print ('For row =',x)
            #res = pd.DataFrame(columns=[pointname])
            z =  int((cusum_control['firstindex'].iloc[x]) )
#             print ('z=',z)
            y = int(cusum_control['lastindex'].iloc[x])
#             print ('y=',y)
            Meanlist = dx[pointname].iloc[z:y + 1]
            StageMean=np.mean(Meanlist)

#             print ('StageMean=', StageMean)
            cusum_control['StageMean'].iloc[x] = StageMean

        #reorder cusumcontrol
        cusum_control = cusum_control[cusum_control['Expanded'].isnull()]
        cusum_control.sort_values('firstindex', ascending=True, inplace=True)
        cusum_control.reset_index()
        #print (cusum_control[['firstindex', 'lastindex','StageMean','conflevel']])

        # find number of entries in cusum_control
        cusumcount = cusum_control['firstindex'].count()


        # get dates into cusumcontrl from df

        for x in range(0,cusumcount ):

            firstindex = int(cusum_control['firstindex'].iloc[x])

            cusum_control['firstdate'].iloc[x] = df[pointdate].iloc[firstindex]

            lastindex = int(cusum_control['lastindex'].iloc[x])

            cusum_control['lastdate'].iloc[x] = df[pointdate].iloc[lastindex]
            
#         print (cusum_control)

        # cusum_control['firstdate'] =  pd.to_datetime(df['firstdate'])
        # cusum_control['lastdate'] =  pd.to_datetime(df['lastdate'])

        # prepare lines for means and dataframe manhatten to hold stage data

        cusum_control['StageMean'] = cusum_control['StageMean'].map(lambda x: '{0:.2f}'.format(x))
        cusum_control['conflevel'] = cusum_control['conflevel'].map(lambda x: '{0:.2f}'.format(x))

        manhatten = pd.DataFrame(columns=[pointdate, 'StageMean', 'conflevel', 'confleveltext'])

        #work out stagemeans

        for y in range(0,cusumcount):
                # why 'k' to identify even and odd rows remembering ranges in python start at 0
                # cusum_control repeats the dates from row to row - First row last date = second row first date
                #
                #k = y + 1
                #using mod function k%1 to work out odd or even
                #if k%1 == 0:  # odd
            firstdate  =  cusum_control['firstdate'].iloc[y]
            lastdate  =  cusum_control['lastdate'].iloc[y]
            firstindex  = int( cusum_control['firstindex'].iloc[y])
            lastindex  =  int(cusum_control['lastindex'].iloc[y])



            Meanlist = df[pointname].iloc[firstindex:lastindex + 1]
            #print ('MeanList1=',Meanlist)
            Datelist = df[pointdate].iloc[firstindex:lastindex + 1]
            #print('Datelist1=',Datelist)
            StageMean=np.mean(Meanlist)
#             print('FirstStage1 Mean =',StageMean)

##                    cusum_control['StageMean'].iloc[y] = StageMean
            decplaces = int(decplaces)
#             print('decplaces', decplaces)
##
            if decplaces == 0:
                    StageMean = int(StageMean)
            if decplaces > 0:
                    StageMean= float(format(StageMean, '.2f'))
                    print(' Stagemean=',StageMean)
            conflevel = cusum_control['conflevel'].iloc[y]

##            confleveltext = 'SM = ' + str(StageMean)  '  % C = ' + str(conflevel)

##            if y == 0:
##                manhatten = manhatten.append({pointdate:firstdate, 'StageMean':StageMean,'conflevel': conflevel} , \
##                                              ignore_index=True)
            if y==0:
                    confleveltext = ' SM = ' + str(StageMean)
                    manhatten = manhatten.append({pointdate:firstdate, 'StageMean':StageMean,'confleveltext': confleveltext} , \
                                                      ignore_index=True)
                    confleveltext = ''
                    manhatten = manhatten.append({pointdate:lastdate, 'StageMean':StageMean,'confleveltext': ' '}, \
                                                      ignore_index=True)
            if y > 0:
                    confleveltext = ' SM = ' + str(StageMean) + '<BR>' + '  % C = ' + str(conflevel)
                    manhatten = manhatten.append({pointdate:firstdate, 'StageMean':StageMean,'conflevel': conflevel, 'confleveltext': confleveltext} , \
                                                              ignore_index=True)
                    manhatten = manhatten.append({pointdate:lastdate, 'StageMean':StageMean,'conflevel': conflevel,'confleveltext': ' '}, \
                                                              ignore_index=True)




##                if k%1 > 1:  #
##                    print ('syd test')
##                    firstdate  =  cusum_control['lastdate'].iloc[y - 1]
##                    lastdate  =  cusum_control['firstdate'].iloc[y]
##                    firstindex  =  int(cusum_control['firstindex'].iloc[y -1])
##                    lastindex  =  int(cusum_control['lastindex'].iloc[y])
##
##                    Meanlist = df[pointname].iloc[firstindex:lastindex + 1]
##                    #print ('MeanList2=',Meanlist)
##                    Datelist = df[pointdate].iloc[firstindex:lastindex + 1]
##                    print('Datelist2=',Datelist)
##                    StageMean=np.mean(Meanlist)
##                    print('FirstSatge2 Mean =',StageMean)
##
##                    cusum_control['StageMean'].iloc[y] = StageMean
##
##
##                    conflevel = cusum_control['conflevel'].iloc[y]
##
##
##
##                    manhatten = manhatten.append({pointdate:firstdate, 'StageMean':StageMean,'conflevel': conflevel, 'confleveltext': confleveltext}, \
##                                                      ignore_index=True)
##                    manhatten = manhatten.append({pointdate:lastdate, 'StageMean':StageMean, 'conflevel': conflevel }, \
##                                                      ignore_index=True)

#         print (manhatten)

        return cusum_control , manhatten

