# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:14:58 2019

@author: Junior
"""

from PIL import Image, ImageDraw
import pandas as pd

from my_functions import data_processing, cal_xy

images = [] # prepare list for create .gif file
df = pd.read_csv('LIDARPoints.csv', header=None) # read LIDARPoints.csv as dataframe
df_flight = pd.read_csv('FlightPath.csv', header=None) # read FlightPath.csv as dataframe
df_flight = df_flight[1::2] # skip id
d = data_processing(df)
loop_index = 0
d_max = [] # this value is for the specified size of the image.

for k, v in d.items(): # loop in dictionaries
    # each round is one sweep
    tmp = []
    for n in v : # for loop every point
        tmp.append(cal_xy([df_flight.iloc[loop_index][0], df_flight.iloc[loop_index][1]], 
                           n[0], n[1]))
    
    ###  find the farthest point  
    merge_data = [i for sub in tmp for i in sub]
    d_max.append(max(merge_data))
    
    # set the convert value 
    d[k] = tuple(tmp)
  
    # set position of the drones as centimeters.
    x_f = int(df_flight.iloc[loop_index][0]*100)
    y_f = int(df_flight.iloc[loop_index][1]*100)
   
    # make frame of image and set size by farthest point plus 100
    # 1 pixel equal to 1 cm
    im = Image.new('RGB', (d_max[loop_index]+100, d_max[loop_index]+100), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # draw drones
    draw.ellipse((x_f-10, y_f-10, x_f+10, y_f+10), fill=(0, 192, 192), outline=(255, 255, 255))
    
    # for loop every point and draw to image
    for dw in d[k] :
        draw.rectangle([dw,(dw[0]+5,dw[1]+5)], fill=(255, 255, 0))
        
    images.append(im) # for create .gif file
    loop_index += 1
    im.show() # show result
    im.close()

# result as .gif file    
images[0].save('images/all_sweep.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=1500, loop=0)  




