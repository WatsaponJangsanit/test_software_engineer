# Test of Software Engineer
Selected Tasks: 1. Display and 5. Mapping 
# Problem Statement
1. **Display** Create a program to provide an appropriate visualization of the drone’s path and the LIDAR data. Ideally, the display should be able to show 1 sweep (1 scan ID) of data in isolation as well as all the sweeps combined together. This can be on separate displays or on the same display (with individual sweeps shown by highlighting for example)  
**Input**​ : LIDARDPoints.csv​ ​ and FlightPath.csv (provided or created from another Task)  
**Output:** On-screen display  
  
5. **Mapping** Use the multiple data sweeps to map out the dimensions of the rooms.  
**Input​ :** LIDARDPoints.csv​ ​ and FlightPath.csv (provided or created)  
**Output:​** Mapping.csv    

# Data processing 
   Convert each line in LIDARPoints.csv to dictionary data, it's like image below 
   ![image](https://user-images.githubusercontent.com/28421585/60667892-951cdd00-9ea5-11e9-9e10-e6b69fc676a1.png)  
   Key is id of sweep, Value is angle of the data point  and the distance of that sweep.  
   
# Strategy formulation
  Use trigonometric principles and use the drones position as the central axis of x, y  
  ![300px-Unit_circle_angles_color svg](https://user-images.githubusercontent.com/28421585/60668596-50924100-9ea7-11e9-8a5f-e4bfa271982e.png)  
  Formula 
   x = (cosθ* distance)/10, y = (sinθ* distance)/10  
  Use the base distance in centimeters then use 1 pixel equal to 1 cm. 
  And because drones position is central axis of x, y  
  the calculation will be the picture below  
  ![image](https://user-images.githubusercontent.com/28421585/60670037-b59b6600-9eaa-11e9-926b-b2430929c0e0.png)  
  That is all required to complete task 1.  
    
  For task 5 use opencv to solve this problem.  
  The first step draws every point on the image.  
  The image will be like this.  
  ![all_points](https://user-images.githubusercontent.com/28421585/60670975-f72d1080-9eac-11e9-8f4f-6a068d6b299f.jpg)  
  And use HoughLinesP function of openCV to detect edge in image  
  The result will be like this  
  ![img_CV2_90](https://user-images.githubusercontent.com/28421585/60671207-905c2700-9ead-11e9-9924-8a183ee1c644.jpg)  
  Then get the value of every edge to create a mapping.csv file  
  

# Installation
1. Download and install python3
 
2. pip install --upgrade pip  

3. pip install -r requirements.txt  
  
4. Open CMD on your git clone local  
   Type "python display.py" to run the task1 file  
   The results will appear according to the number of sweeps(34 times)  
   And create .gif file of all sweeps.  
     
5. Open CMD on your git clone local 
   Type "python mapping.py" to run the task5 file   
   The results will be Mapping.csv file and Detected edge Image  
     

## Output
  Tasks: 1. Display  
![resize](https://user-images.githubusercontent.com/28421585/60665467-7f0c1e00-9e9f-11e9-9d62-860a73ad0125.gif)

  Tasks: 5. Mapping  
   (xstart, ystart, xend, ystart)  
![image](https://user-images.githubusercontent.com/28421585/60665231-ea092500-9e9e-11e9-9d3c-c54d2b3ea86d.png)  

 
