import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
import plotly
from datetime import datetime , timedelta

@anvil.server.callable
def save_as_json(chartid, fig , no_of_steps ):
#    json_object = plotly.io.to_json(fig)
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     fig_json = plotly.io.to_json(fig)
#     json_object = py.io.to_json(self.plot_1.data, 'plot.json')
#    print("fig_json=",json_object)

   anvil.server.call('save_chart', chartid, graphJSON, no_of_steps)
#    print('json saved')
    
    
@anvil.server.callable
def load_from_json(chartid):
    # some way to get it from the data table. obviously change as needed
     
     t = app_tables.charts.get(id= chartid)
     chart = t['json']
     fig = json.loads(chart)
#      print(fig)  
     return fig
    
    
@anvil.server.callable
def save_chart(chartid, json_object,no_of_steps):
#     print(img_object)
    then = datetime.now()
    t = app_tables.charts.get(id= chartid)
 
    t['json'] = json_object
    t['Chart_last_saved'] = datetime.now()
    t['no_of_steps'] = no_of_steps
#     print("Save Json time " + str(datetime.now() - then) + '\n')
 
# @anvil.server.callable
# def check_json_dataexistsinCharts(chartid):
#     tcharts = app_tables.charts.get(id = chartid)
#     json = tcharts['json']
# #     print('json=',json)
#     return  json


