import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import plotly.graph_objects as go
# from ..Bootstrap.get_manhatten_data import get_pdcalls_manhatten
# from Chart_Maintenance.Loading_Saving_Charts_JSON import save_as_json

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def charts(self, **event_args):
      import json
      import plotly as py
      chart_copy = dict(list(self.item))
      chart_title = chart_copy['title']
      #     csvname =self.item['category']
      #     print("Chart Title =", chart_title)
      if chart_title == None:
            alert(" Please select a chart from the dropdown")
      else:
          # get chartid
          chart_copy = dict(list(self.item))
          print(chart_copy['id'])
          chartid = chart_copy['id']
          
          create_chart(self,chart_copy)

        
def create_chart(self, chart_copy):
    
          start_date = chart_copy['astart_date']
          print(start_date)
          end_date = chart_copy['aend_date']
        #                   start_date = self.start_date_picker.date
        #                   end_date = self.end_date_picker.date
          conf_level_text = chart_copy['conf_limit_text']
          moving_avg =  chart_copy['mov_avg']
        #                   chart_title = self.drop_down_1.selected_value
          chart_title = chart_copy['title']
          chartid = chart_copy['id']
#           print('chartid=',chartid)
          scatter = anvil.server.call('get_pdcalls', chartid, start_date, end_date)
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
#           print('Generated chart afresh=',scatter)
#           chart_copy = dict(list(self.item))
#           print(chart_copy['id'])
#           chartid = chart_copy['id']
        # saves json and updates the chart last updated field
#           anvil.server.call('save_as_json', chartid, self.plot_1.data)


def step_change_bulk_update_in_background():

          charts  = anvil.server.call('list_charts_not_archived') # when filename exist
          for row in charts:
                print ('id =', row['id'])
                chartid = row['id']
                #  Get Chart last updated Date 
                Chart_last_saved = anvil.server.call('get_Chart_last_saved',chartid)
                print('Chart_last_saved=',Chart_last_saved)
              
              # get casv last updted Date
                csvdatetime_loaded = anvil.server.call('get_csvdatetime_loaded',chartid)      
                print('csvlast_uploaded=',csvdatetime_loaded)
                
    #           # check for change in conf_limit 
                conf_limit_text, last_conf_limit = anvil.server.call('get_conf_limits', chartid)
                print('conf_limit_text=',conf_limit_text)
                print('last_conf_limit=',last_conf_limit)
              #  (conf_limit_text == last_conf_limit)  catches changes in conf limit set by form dropdown -  no change -  load json
                # (Chart_last_saved > csvdatetime_loaded) catches when the csv file is updated - no update load json otherwise recalculate chart
             
                manconf, no_of_steps = anvil.server.call('launch_one_crawler', chartid)
                # saves json and updates the chart last updated field
                anvil.server.call('save_as_json', chartid, manconf, no_of_steps)
                print('Chart regenerated in background=', chartid)
                
                
def step_changes(self, chart_position, **event_args):
      import json
      import plotly as py
      
      
      
      chart_copy = dict(list(self.item))
      chart_title = chart_copy['title']
      #     csvname =self.item['category']
      #     print("Chart Title =", chart_title)
      if chart_title == None:
            alert(" Please select a chart from the dropdown")
      else:
          # get chartid
          chart_copy = dict(list(self.item))
          print(chart_copy['id'])
          chartid = chart_copy['id']
          create_step_chart(self, chart_copy , chart_position)
             # update last conf limit 
        
          start_step_changes = datetime.now()
          conf_limit_text, last_conf_limit = anvil.server.call('get_conf_limits', chartid) 
          t = app_tables.charts.search(id = chartid)
          for row in t:
              if row['conf_limit_text'] != None:
                  current_conf_limit =row['conf_limit_text'] 
                  row['last_conf_limit'] =  current_conf_limit  
          print('conf_limit_text=',conf_limit_text)
          print('last_conf_limit=',last_conf_limit)
          print("Step_change Time: " + str(datetime.now() - start_step_changes) + '\n')
#         # Get Chart last updated Date 
#           Chart_last_saved = anvil.server.call('get_Chart_last_saved',chartid)
#           print('Chart_last_saved=',Chart_last_saved)
         
#         # get casv last updted Date
#           csvdatetime_loaded = anvil.server.call('get_csvdatetime_loaded',chartid)
#           print('csvlast_uploaded=',csvdatetime_loaded)
          
#           if csvdatetime_loaded == None:
#               alert(" No csv file exist!")
#           else:
# #         # check if json data exist in Charts table fro chartid
        
#               NoJSONinchartTable = anvil.server.call('check_json_dataexistsinCharts',chartid)
#               print('NoJSON exists?',NoJSONinchartTable)
#             # if no json calcuate scatter, saveit to tchart table. update chart date, draw chart
#               if (Chart_last_saved) == None:
#                   self.plot_1.visible = True
#                   self.plot_1.data  = create_step_chart(self, chart_copy)
#                   print('Chart_last_saved) == None chart generated for first time')
#               else:
                
#                   if (Chart_last_saved < csvdatetime_loaded) :
#                         self.plot_1.visible = True
#                         self.plot_1.data  = create_step_chart(self, chart_copy)
#                         print('Chart_last_saved < csvdatetime_loaded - chart regenerated - new csv date')
                         
#                   else:
                        
#                       fig = anvil.server.call('load_from_json', chartid)
                      
#                       print('Returned from table=',fig)
#                       print('Chart_last_saved > csvdatetime_loaded - loaded from Json')
#                       self.plot_1.visible = True
#                       self.plot_1.data = fig
                      
          return self.plot_1.data          

def create_step_chart(self, chart_copy, chart_position):
            
            chartid = chart_copy['id']
            print('Chart id=', )
            print(type(chartid))
            chart_title = chart_copy['title']
        # Get Chart last updated Date 
            Chart_last_saved = anvil.server.call('get_Chart_last_saved',chartid)
            print('Chart_last_saved=',Chart_last_saved)
#             if  Chart_last_saved == None:
#                Chart_last_saved = datetime.now()
          # get casv last updted Date
            csvdatetime_loaded = anvil.server.call('get_csvdatetime_loaded',chartid)      
            print('csvlast_uploaded=',csvdatetime_loaded)
            
#           # check for change in conf_limit 
            conf_limit_text, last_conf_limit = anvil.server.call('get_conf_limits', chartid)
            print('conf_limit_text=',conf_limit_text)
            print('last_conf_limit=',last_conf_limit)
           #  (conf_limit_text == last_conf_limit)  catches changes in conf limit set by form dropdown -  no change -  load json
            # (Chart_last_saved > csvdatetime_loaded) catches when the csv file is updated - no update load json otherwise recalculate chart
    #         if  Chart_last_saved  == None:
    #             print('Start of get_pdcalls_manhatten '+str(datetime.now()))
    #             manconf, no_of_steps = anvil.server.call('get_pdcalls_manhatten', chartid)
    #             print('No of Steps=', no_of_steps)
    #             print('End of get_pdcalls_manhatten '+str(datetime.now()))
    #             anvil.server.call('save_as_json', chartid, manconf, no_of_steps)
    #         else:
    #             if ((Chart_last_saved > csvdatetime_loaded) and (conf_limit_text == last_conf_limit))  :
                     
    #                   manconf  = anvil.server.call('load_from_json', chartid)
                      
    #                   no_of_steps = anvil.server.call('get_no_of_steps', chartid)
    #                   print('manconf=',manconf)
    #                   conf_limit = chart_copy['conf_limit_text']    
    # #                       print('Returned from table=',fig)
    #                   print('Chart_last_saved > csvdatetime_loaded - loaded from Json')
    # #                       self.plot_1.visible = True
    # #                       self.plot_1.data = fig
                          
    #             else:
            start_load_data = datetime.now() 
            manconf, no_of_steps = anvil.server.call('get_pdcalls_manhatten', chartid)
  #                         print("get_pdcalls_manhatten Time: " + str(datetime.now() - start_load_data) + '\n')   
              
            print('No of Steps=', no_of_steps)

                        # anvil.server.call('save_as_json', chartid, manconf, no_of_steps)
            if chart_position == 1:
                  self.plot_1.visible = True 
      
                  self.plot_1.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b4"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_1.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_1.layout.title =  chart_title + " (" + str(chartid) + ")" + " " + "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_1.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_1.data = manconf 
                        
                  pass
            if chart_position == 2:
                  self.plot_2.visible = True 
      
                  self.plot_2.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b4"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_2.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_2.layout.title =  chart_title + " (" + str(chartid) + ")" + " " + "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_2.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_2.data = manconf 
                        
                  pass 
            if chart_position == 3:
                  self.plot_3.visible = True 
      
                  self.plot_3.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b4"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_3.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_3.layout.title =  chart_title + " (" + str(chartid) + ")" +  " " + "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_3.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_3.data = manconf 
        
            if chart_position == 4:
                  self.plot_4.visible = True 
      
                  self.plot_4.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b4"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_4.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_4.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_4.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_4.data = manconf 
                                                
                  pass
            if chart_position == 5:
                  self.plot_5.visible = True 
      
                  self.plot_5.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_5.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_5.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_5.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_5.data = manconf 
        
            if chart_position == 6:
                  self.plot_6.visible = True 
      
                  self.plot_6.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_6.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_6.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_6.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_6.data = manconf 
        
            if chart_position == 7:
                  self.plot_7.visible = True 
      
                  self.plot_7.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_7.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_7.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_7.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_7.data = manconf                                    
                   
            if chart_position == 8:
                  self.plot_8.visible = True 
      
                  self.plot_8.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_8.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_8.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_8.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_8.data = manconf 
        
            if chart_position == 9:
                  self.plot_9.visible = True 
      
                  self.plot_9.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_9.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_9.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_9.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_9.data = manconf    
            if chart_position == 10:
                  self.plot_10.visible = True 
      
                  self.plot_10.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_10.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_10.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_10.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_10.data = manconf   
                  pass 
            if chart_position == 11:
                  self.plot_11.visible = True 
      
                  self.plot_11.layout.yaxis =  dict(title=chart_title,
                                                      titlefont=dict(color="#1f77b5"),
                                                      tickfont=dict(color="#1f77b4"), 
                                                      )
                  self.plot_11.layout.xaxis = dict(tickangle=45)    
                  
                  self.plot_11.layout.title =  chart_title + " (" + str(chartid) + ")" + " " +  "with Conf. Limit =" + " " + str(conf_limit_text) +"%" + " created at " + datetime.now().strftime('%d %B %Y %H:%M')    + " (Note: " + str(no_of_steps) + " steps shown of a  Max. of 15 steps examined)" 
            #           (Change Conf. Limit = {str(conf_limit)}%) Creation Date: {datetime.now().strftime('%d %B %Y %H:%M')}")
                
                  self.plot_11.layout.yaxis2 = dict(title="Cusum",
                                                  titlefont=dict(color='green'),
                                                  tickfont=dict(color='green'),
                                                  overlaying="y",
                                                  side='right'
                                                  )
                      
      
                  self.plot_11.data = manconf   
                  pass      

def trends(self, **event_args):
  chart_type = 'trends'
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
    data = anvil.server.call('ols_plot', chartid, chart_type)  # get regression line data
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
def range_cusum(self, **event_args):
  chart_type = 'range_cusum'
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
    data = anvil.server.call('ols_plot', chartid, chart_type)  # get regression line data
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
    # self.plot_1.layout.yaxis = dict(title=chart_title,
    #                                     titlefont=dict(color="#1f77b4"),
    #                                     tickfont=dict(color="#1f77b4"), 
    #                                     )
    self.plot_1.layout.xaxis = dict(tickangle=45)    
    self.plot_1.layout.title = chart_title + " created at " + datetime.now().strftime('%d %B %Y %H:%M')     
    self.plot_1.data=data
    pass      


def chart_cusum(self, **event_args):
  chart_type = 'chart_cusum'
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
    data = anvil.server.call('ols_plot', chartid, chart_type)  # get regression line data
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
    # self.plot_1.layout.yaxis = dict(title=chart_title,
    #                                     titlefont=dict(color="#1f77b4"),
    #                                     tickfont=dict(color="#1f77b4"), 
    #                                     )
    self.plot_1.layout.xaxis = dict(tickangle=45)    
    self.plot_1.layout.title = chart_title + " created at " + datetime.now().strftime('%d %B %Y %H:%M')     
    self.plot_1.data=data
    pass      
def range(self, **event_args):
  chart_type = 'range'
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
    data = anvil.server.call('ols_plot', chartid, chart_type)  # get regression line data
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
    # self.plot_1.layout.yaxis = dict(title=chart_title,
    #                                     titlefont=dict(color="#1f77b4"),
    #                                     tickfont=dict(color="#1f77b4"), 
    #                                     )
    self.plot_1.layout.xaxis = dict(tickangle=45)    
    self.plot_1.layout.title = chart_title + " created at " + datetime.now().strftime('%d %B %Y %H:%M')     
    self.plot_1.data=data
    pass  
def tables(self, **event_args):
  import json
  import plotly as py
  chart_copy = dict(list(self.item))
  chart_title = chart_copy['title']
  #     csvname =self.item['category']
  #     print("Chart Title =", chart_title)
  if chart_title == None:
        alert(" Please select a chart from the dropdown")
  else:
      # get chartid
      chart_copy = dict(list(self.item))
      print(chart_copy['id'])
      chartid = chart_copy['id']

      create_table(self,chartid)

def create_table(self, chartid):
    
      dfcsv, nameCol, dateCol, title, conf_limit, format_col = anvil.server.call('ols_data', chartid)
      table = dfcsv.to_dict(orient='records')
      scatter = [go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ]
        
      start_date = chart_copy['astart_date']
      end_date = chart_copy['aend_date']
      #                   start_date = self.start_date_picker.date
      #                   end_date = self.end_date_picker.date
      conf_level_text = chart_copy['conf_limit_text']
      moving_avg =  chart_copy['mov_avg']
      #                   chart_title = self.drop_down_1.selected_value
      chart_title = chart_copy['title']
      chartid = chart_copy['id']
#       print('chartid=',chartid)
      dfcsv, nameCol, dateCol, title, conf_limit, format_col = anvil.server.call('ols_data', chartid)
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
        # saves json and updates the chart last updated field
      #           anvil.server.call('save_as_json', chartid, self.plot_1.data)
      
      