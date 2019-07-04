# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:14:58 2019

@author: Junior
"""

from PIL import Image, ImageDraw
import pandas as pd
import math

images = [] # prepare list for create .gif file

df = pd.read_csv('LIDARPoints.csv', header=None) # read LIDARPoints.csv as dataframe
df_flight = pd.read_csv('FlightPath.csv', header=None) # read FlightPath.csv as dataframe


##################################################
############## data processing start #############
df_flight = df_flight[1::2] # skip id
s_num = int(df.iloc[0][1]) # number of data lines of the first ID
d = {} # prepare dictionaries to make data management easier
tmp_list = [] #to rest angle of the data point and the distance  of each ID
c = -1 #for countdown the line number
for index, row in df.iterrows():
    if s_num == c :
        d[int(tmp_list[0][0])] = tmp_list[1:]
        s_num = int(row[1])
        c = -1
        tmp_list = []
    elif index == df.shape[0]-1: # last id
        tmp_list.append(list(row))
        d[int(tmp_list[0][0])] = tmp_list[1:]
    tmp_list.append(list(row))
    c += 1

############## data processing end ###############
##################################################
    
    
def cal_xy(center, degrees, distance): # this function converts the distance into centimeters
    
    # use trigonometry and convert millimeters to centimeters
    xy_tuple = [abs(int(round(math.cos(math.radians(degrees))*distance,2)/10)), 
                abs(int(round(math.sin(math.radians(degrees))*distance,2)/10))]
    
    # convert meters to centimeters
    center_x = int(center[0]*100)
    center_y = int(center[1]*100)
    
    ### Because drones are the central axis x, y Therefore, the degree must be specified to draw on the image.
    if 0 <degrees < 90 :
        xy_tuple = (center_x + xy_tuple[0],center_y - xy_tuple[1])
    elif 90 <degrees < 180 :
        xy_tuple = (center_x - xy_tuple[0],center_y - xy_tuple[1])
    elif 180 <degrees < 270 :
        xy_tuple = (center_x - xy_tuple[0],center_y + xy_tuple[1])
    else:
        xy_tuple = (center_x + xy_tuple[0],center_y + xy_tuple[1])

    return(xy_tuple)


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
   
    # make frame of image and set size by farthest point plus 500
    # 1 pixel equal to 1 cm
    im = Image.new('RGB', (d_max[loop_index]+500, d_max[loop_index]+500), (0, 0, 0))
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




