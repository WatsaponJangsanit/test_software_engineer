# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:14:58 2019

@author: Junior
"""

from PIL import Image, ImageDraw
import pandas as pd
import math

images = []

df = pd.read_csv('LIDARPoints.csv', header=None)
df_flight = pd.read_csv('FlightPath.csv', header=None)
df_flight = df_flight[1::2]
s_id = int(df.iloc[0][0])
s_num = int(df.iloc[0][1])
d = {}
tmp_list = []

c = -1
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

def cal_xy(center, degrees, distance):
    xy_tuple = [abs(int(round(math.cos(math.radians(degrees))*distance,2)/10)),
                abs(int(round(math.sin(math.radians(degrees))*distance,2)/10))]
    if 0 <degrees < 90 :
        xy_tuple = (center[0] + xy_tuple[0],center[1] - xy_tuple[1])
    elif 90 <degrees < 180 :
        xy_tuple = (center[0] - xy_tuple[0],center[1] - xy_tuple[1])
    elif 180 <degrees < 270 :
        xy_tuple = (center[0] - xy_tuple[0],center[1] + xy_tuple[1])
    else:
        xy_tuple = (center[0] + xy_tuple[0],center[1] + xy_tuple[1])

    return(xy_tuple)
    
loop_index = 0
d_max = []

for k, v in d.items():
    tmp = []
    for n in v :
        tmp.append(cal_xy([int(df_flight.iloc[loop_index][0]*100),int(df_flight.iloc[loop_index][1]*100)], 
                           n[0], n[1]))
        
    merge_data = [i for sub in tmp for i in sub]
    d_max.append(max(merge_data))
    d[k] = tuple(tmp)
    

  
    x_f = int(df_flight.iloc[loop_index][0]*100)
    y_f = int(df_flight.iloc[loop_index][1]*100)
   
    im = Image.new('RGB', (d_max[loop_index]+500, d_max[loop_index]+500), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    draw.ellipse((x_f-10, y_f-10, x_f+10, y_f+10), fill=(0, 192, 192), outline=(255, 255, 255))
    for dw in d[k] :
        draw.rectangle([dw,(dw[0]+5,dw[1]+5)], fill=(255, 255, 0))
    images.append(im)
    loop_index += 1
#    im.show()
#    im.close()
    
images[0].save('images/all_sweep.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=1500, loop=0)  




