import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server

def trends(self, **event_args):
  """This method is called when the button is clicked"""
  chart_copy = dict(list(self.item))
  chartid = chart_copy['id']
  chart_title = chart_copy['title']
#   check if chart title exists  
#for info find the saved moving average
  moving_average = chart_copy['mov_avg']
  print('Moving average=', moving_average)
  if chartid == None:
        alert(" Please select a chart from the dropdown")
  else:
    data = anvil.server.call('ols_plot', chartid)  # get regression line data
#       data=anvil.server.call('ols_plot')
    conf_limit =""
#       alert(content=Form5(data,chart_title, conf_limit),
#               title =chart_title + " " +"Trends",
#               large=True,
#               buttons=[
#                      ("Cancel", False)
                    
#                    ])
    self.plot_1.visible = True
#     self.card_1.visible = False
#       self.label_10.visible = False
#       self.trends.foreground = '#ee67a1'
#       self.button_2.foreground = '#5ba1ec'
#       self.all_points.foreground = '#5ba1ec' 
#       self.change_points.foreground = '#5ba1ec' 
    self.plot_1.layout.yaxis = dict(title=chart_title,
                                        titlefont=dict(color="#1f77b4"),
                                        tickfont=dict(color="#1f77b4"), 
                                        )
    self.plot_1.layout.xaxis = dict(tickangle=45)    
    self.plot_1.layout.title = chart_title + " created at " + datetime.now().strftime('%d %B %Y %H:%M')     
    self.plot_1.data=data
    pass

