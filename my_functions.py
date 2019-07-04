# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 19:17:42 2019

@author: Junior
"""

import math
##################################################
############## data processing start #############
def data_processing(df):
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
    return(d)

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