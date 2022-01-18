import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from plotly.subplots import make_subplots
from .supportsparklines import create_sparkline
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
def get_Changes_sparklines():
    
   
    fig = make_subplots(rows=10, cols=1 , row_heights=[0.1, 0.1, 0.1, 0.1,0.1,0.1, 0.1, 0.1, 0.1,0.1], subplot_titles = ("Defects Detected (102)", \
                                                 "Problem Cases (44)","Config Cases (45)", "Interfaces Cases (46)","Printing Cases (47)","How to Cases (78)", \
                                                  "NPS Scores (51)","NPS responses (79)","Expert Helps (66)"))
   
  #================All Cases Arriving =========================================================================  
    chartid = 102
    rowno = 1
    color = 'blue'
    
    
    mean1, dfcsv1, nameCol1, dateCol1, title1, conf_limit1, formatCol1  = create_sparkline(chartid, rowno , color)
    name_of_chart = title1
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1['Mov_avg8'],
                          mode='lines',
                          name=name_of_chart,
                          line=dict(
        color=color,
        width=2,
        ),
        visible=True),
        row=rowno, col=1)
    fig.add_trace(go.Scatter(x=dfcsv1[dateCol1],
                        y = dfcsv1['Mean'] ,
                          mode='lines',
                          name= name_of_chart + ' ' + 'average  =' + str(round(mean1,0)),
                          line=dict(
        color=color,
        width=1,
        dash='dash'                   
        ),
        visible=True),
        row=rowno, col=1) 

