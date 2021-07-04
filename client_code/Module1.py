import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


def create_chart():
    
#           start_date = chart_copy['astart_date']
#           end_date = chart_copy['aend_date']
#         #                   start_date = self.start_date_picker.date
#         #                   end_date = self.end_date_picker.date
#           conf_level_text = chart_copy['conf_limit_text']
#           moving_avg =  chart_copy['mov_avg']
#         #                   chart_title = self.drop_down_1.selected_value
#           chart_title = chart_copy['title']
#           chartid = chart_copy['id']
# #           print('chartid=',chartid)
          chartid = 78
  
  
          scatter = anvil.server.call('get_pdcalls', chartid)
          conf_limit =""
        #         alert(content=Form5(scatter,chart_title,conf_limit),
        #               title =chart_title + " " + "Plot of Points",
        #               large=True,
        #               buttons=[
        #                      ("Cancel", False)
                        
        #                    ])
        
          self.plot_1.visible = True
        #           self.card_1.visible = False
        #                   self.label_10.visible = False
        #                   self.all_points.foreground = '#ee67a1'
          self.plot_1.layout.yaxis = dict(title=chart_title,
                                              titlefont=dict(color="#1f77b4"),
                                              tickfont=dict(color="#1f77b4"), 
                                              )
          self.plot_1.layout.xaxis = dict(tickangle=45)    
        
          self.plot_1.layout.title = chart_title + " "  +  " created at " + datetime.now().strftime('%d %B %Y %H:%M') 
          self.plot_1.layout.yaxis2 = dict(title="Cusum",
                                          titlefont=dict(color='green'),
                                          tickfont=dict(color='green'),
                                          overlaying="y",
                                          side='right'
                                          )
          
          
          
          self.plot_1.data = scatter
          print('Generated chart afresh=',scatter)
          chart_copy = dict(list(self.item))
          print(chart_copy['id'])
          chartid = chart_copy['id']
