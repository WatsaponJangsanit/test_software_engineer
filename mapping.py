# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 18:46:31 2019

@author: Junior
"""


import pandas as pd
import csv
import cv2 
import numpy as np 
import time

from my_functions import data_processing, cal_xy
from PIL import Image, ImageDraw


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
         
    loop_index += 1

# make frame of image and set size by farthest point plus 100
# 1 pixel equal to 1 cm
im = Image.new('RGB', (d_max[0]+100, d_max[0]+100), (0, 0, 0))
draw = ImageDraw.Draw(im)


# for loop every point and draw to image
for n in d :
    for dw in d[n]:
        draw.rectangle([dw,(dw[0]+5,dw[1]+5)], fill=(255, 255, 0))
    
im.save("images/all_points.jpg", "JPEG", quality=95, optimize=True, progressive=True)

time.sleep(3)


img = cv2.imread('images/all_points.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 30  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 20  # minimum number of pixels making up a line
max_line_gap = 50  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),  min_line_length, max_line_gap)


with open('​Mapping.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile)
    for line in lines:
        for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)   
                filewriter.writerow([str(x1*10), 
                                     str(y1*10), 
                                     str(x2*10), 
                                     str(y2*10)])

         
lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

cv2.imwrite('images/img_CV2_90.jpg', lines_edges, [int(cv2.IMWRITE_JPEG_QUALITY), 90])



    
    