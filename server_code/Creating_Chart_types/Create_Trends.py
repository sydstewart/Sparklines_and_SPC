import anvil.email
import tables
from tables import app_tables
import anvil.server
import io
import plotly.graph_objects as go
import datetime as dt
import json
import anvil.tables.query as q
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime , timedelta
import plotly
import pandas as pd
import numpy as np
import anvil.media 
import anvil.server
from ..Creating_Chart_types.Getting_Data_for_Charts import ols_data 
from sklearn.linear_model import LinearRegression


@anvil.server.callable
def ols_plot(chartid):
  dfcsv, nameCol, dateCol, title, conf_limit, format_col, noteCol = ols_data(chartid)
  print('dfcsv', dfcsv)
  print('++++++++++++++++++++++++++++++++++++++++++++')
  print(dfcsv[dateCol],dfcsv['UCL'])
  #Convert to a string to y - m -d
  dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol]).dt.strftime('%Y-%m-%d')
  #Change string to date column to allow calculation of days between base date and column date
  dfcsv[dateCol]= pd.to_datetime(dfcsv[dateCol])
  dfcsv.info()
  
  X=dfcsv[dateCol] # dates
#   print(X)
  #set a base date
  base_date = pd.Timestamp('1900-01-01')
  
  #convert dates to a number based on days
  intdfcsv = df = pd.DataFrame()
  # calculate days from base date
  dfcsv['basedate']  = pd.Timestamp('1900-01-01')
  dfcsv['time since'] = (dfcsv[dateCol] - base_date).dt.days
#   dfcsv['time since'] = dfcsv[dateCol].sub(dfcsv['basedate'], axis=0)
#   dfcsv['time since'] = dfcsv[dateCol] - dfcsv['basedate'] 
#   dfcsv['time since'] = dfcsv[dateCol].map(lambda date : (pd.Timestamp(date) - base_date).days )
#   intdfcsv[dateCol] = dfcsv[[dateCol].apply(lambda x: (x.name.to_datetime() - basedate).days)
#   df['time since'] = df.apply(lambda x: (x.name.to_datetime() - basedate).days, axis=1)                          
# #   dfcsv['time since'] = dfcsv.apply(lambda x: (x.name.to_datetime() - basedate).days, axis=1)
#   print(dfcsv['time since'])
  X = dfcsv['time since'] # based on numbers
  Y=dfcsv[nameCol]
  
  x = np.array(X).reshape((-1, 1))
  y = np.array(Y)
  model = LinearRegression().fit(x, y)
  y_pred = model.predict(x)
  
  # Convert date column back to string
  dfcsv[dateCol].dt.date
#   print(dfcsv[dateCol])
  # Change format of string to %d/%m/%Y
#   dfcsv[dateCol] = dfcsv[dateCol].dt.strftime('%d/%m/%Y')
#   dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol]).dt.strftime('%d-%m-%Y')
  X=dfcsv[dateCol]
  print ('UCL', dfcsv['UCL'])
  data = [
  go.Scatter(
    x = dfcsv[dateCol],
    y = dfcsv[nameCol],
    mode='markers+ lines',
    name='Data points'
  ),
  go.Scatter(
    x = dfcsv[dateCol],
    y = y_pred,
    mode='lines',
    name='Linear Trend'),
  go.Scatter(
    x = dfcsv[dateCol],
    y = dfcsv['mean'],
    mode='lines',
    name='Mean'),
  go.Scatter(
    x = dfcsv[dateCol],
    y = dfcsv['UCL'],
    mode='lines',
    name='UCL'),
  go.Scatter(
    x = dfcsv[dateCol],
    y = dfcsv['Mov_avg8'],
    mode='lines',
    name='Moving average'
  )
]

  return data