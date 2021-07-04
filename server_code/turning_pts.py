import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
import pandas as pd
import plotly.graph_objects as go
from . import get_csv_data
import io
import numpy as np
import anvil.mpl_util


@anvil.server.callable
def get_csv_data():
      fileName ='nps.csv'
      df = csv_data_1(fileName)
      
      print (df)
      return df
                 

       
@anvil.server.callable
def turning_pts():
      fileName ='nps.csv'
      df = csv_data_1(fileName)
      
#       df = pd.DataFrame({'Col A': [0,12,6], 'Date':['01/01/2020','01/02/2020','01/03/2021']  })
       
#       df["TP"] = ((df["Col A"].shift(-2) < df["Col A"].shift(-1)) & 
#               (dfcsv["Col A"].shift(-1) < dfcsv["Col A"]) &
#               (df["Col A"].shift( 1) < df["Col A"]) &
#               (df["Col A"].shift( 2) < df["Col A"].shift( 1))).astype(int)
#       print(df[['TP' , 'Col A']])
      scatter = go.Scatter(x= df['Date_entered'],
                           y = df['NPScusum'],
                           name="NPS cusum",
                           line=dict(color='green', width=2))
                 

      return scatter 
    
@anvil.server.callable
def csv_data_1(fileName):

      m=app_tables.my_files.get(name = fileName)['media_obj'] 
#       t= app_tables.charts.get(file_name=fileName)
      dayfirst = True
      dateCol = 'Date_entered'
      print('DayFirst', dayfirst)
#         dayfirst is FALSE for DD/MM  = MM/DD True
      #Read in data file csv
      dfcsv = pd.read_csv(io.BytesIO(m.get_bytes()),parse_dates=[dateCol] , dayfirst=True, infer_datetime_format=True)
      dfcsv[dateCol] = pd.to_datetime(dfcsv[dateCol])
#       print(dfcsv)
      dfcsv['meanNPS'] = dfcsv['NPS'].mean()
      dfcsv['cusumdiff']= dfcsv['NPS'] - dfcsv['meanNPS']
      dfcsv['NPScusum'] = dfcsv['cusumdiff'].cumsum()
      dfcsv["TP"] = ((dfcsv["NPScusum"].shift(-2) < dfcsv["NPScusum"].shift(-1)) & 
              (dfcsv["NPScusum"].shift(-1) < dfcsv["NPScusum"]) &
              (dfcsv["NPScusum"].shift( 1) < dfcsv["NPScusum"]) &
              (dfcsv["NPScusum"].shift( 2) < dfcsv["NPScusum"].shift( 1))).astype(int)
      print(dfcsv[['Date_entered' , 'TP']])
       
      dfcsv["TP"] = 1
      print(dfcsv)
#      
      
 
      return dfcsv


import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def rdp(points, epsilon):
    # get the start and end points
    start = np.tile(np.expand_dims(points[0], axis=0), (points.shape[0], 1))
    end = np.tile(np.expand_dims(points[-1], axis=0), (points.shape[0], 1))

    # find distance from other_points to line formed by start and end
    dist_point_to_line = np.abs(np.cross(end - start, points - start, axis=-1)) / np.linalg.norm(end - start, axis=-1)
    # get the index of the points with the largest distance
    max_idx = np.argmax(dist_point_to_line)
    max_value = dist_point_to_line[max_idx]

    result = []
    if max_value > epsilon:
        partial_results_left = rdp(points[:max_idx+1], epsilon)
        result += [list(i) for i in partial_results_left if list(i) not in result]
        partial_results_right = rdp(points[max_idx:], epsilon)
        result += [list(i) for i in partial_results_right if list(i) not in result]
    else:
        result += [points[0], points[-1]]
  
    return result

@anvil.server.callable
def rdpexample():
# if __name__ == "__main__":

    fig, ax = plt.subplots()
  
    min_x = 0
    max_x = 5
    
    xs = np.linspace(min_x, max_x, num=200)
    ys = np.exp(-xs) * np.cos(2 * np.pi * xs)
    sample_points = np.concatenate([
        np.expand_dims(xs, axis=-1),
        np.expand_dims(ys, axis=-1)
    ], axis=-1)
    
    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(min_x, max_x), ylim=(-1, 1))
    plt.xlabel("x")
    plt.ylabel("y")
    text_values = ax.text(
        0.70,
        0.15,
        "",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round',
                  facecolor='wheat',
                  alpha=0.2)
    )
    original_line, = ax.plot(xs, ys, lw=2, label=r"$y = e^{-x}cos(2 \pi x)$")
    simplified_line, = ax.plot([], [], lw=2, label="simplified", marker='o', color='r')
    
#     # # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=21,
    interval=1000,
    repeat=True
    )
#     plt.plot(xs, ys, label = "line 1")
#     plt.plot(xs, ys, label = "line 2")
    
#     ax.plot([], [], label='Simplified Line', color='red', linestyle='dashed')
    # initialization function: plot the background of each frame
    plt.legend()
    plt.show()
    return anvil.mpl_util.plot_image()
  
def init():
    simplified_line.set_data(xs, ys)
    return original_line, simplified_line, text_values

# animation function.  This is called sequentially
def animate(i):
    epsilon = 0 + (i * 0.1)
    simplified = np.array(rdp(sample_points, epsilon))
    print(f"i: {i}, episilon: {'%.1f' % epsilon}, n: {simplified.shape[0]}")
    simplified_line.set_data(simplified[:, 0], simplified[:, 1])
    text_values.set_text(fr"$\epsilon$: {'%.1f' % epsilon}, $n$: {simplified.shape[0]}")
    return original_line, simplified_line, text_values


