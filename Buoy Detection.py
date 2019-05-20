import cv2
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import math


# Detection for Orange buoys in the generated results

# Read the image, apply erosion and dilation to remove noise
# and used contour detection to get the buoy's location and
# fit a circle around the buoy

def detect_orange_buoy(i, frame):    
    result = cv2.imread('result_orange/result('+str(i)+').png',1)
#     frame = cv2.imread('Frames/Frames/'+str(i)+'.jpg',1)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(result,kernel,iterations = 2)
    center = 0 
    radius = 0
    kernel2 = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(result,kernel2,iterations = 3)

    thresh = cv2.cvtColor(dilation, cv2.COLOR_RGB2GRAY)

    _ , contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(result, contours, -1, (70,170,247), 3)

    cnts = sorted(contours, key = cv2.contourArea, reverse = True)
    try:
        (x,y),radius = cv2.minEnclosingCircle(cnts[0])

        center = (int(x),int(y))
        radius = int(radius)
        #     cv2.circle(result,center,radius,(70,170,247),2)
        cv2.circle(frame,center,radius,(70,170,247),2)
    except:
        pass


# Function to detect yellow buoys

def detect_yellow_buoy(i, frame):
    result = cv2.imread('result_yellow/result('+str(i)+').png')
#     frame = cv2.imread('Frames/Frames/'+str(i)+'.jpg',1)
    kernel = np.ones((10,10),np.uint8)
    kernel2 = np.ones((2,2),np.uint8)
    center = 0 
    radius = 0
    # erosion = cv2.erode(result,kernel2,iterations = 2)
    # dilation = cv2.dilate(erosion,kernel2,iterations = 10)

    for j in range(15):
        closing = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)

    dilation = cv2.dilate(closing,kernel2,iterations = 4)    
    thresh = cv2.cvtColor(dilation, cv2.COLOR_RGB2GRAY)

    _ , contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(result, contours, -1, (0,255,255), 3)
    try:
        cnts = sorted(contours, key = cv2.contourArea, reverse = True)
        (x,y),radius = cv2.minEnclosingCircle(cnts[0])
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(frame,center,radius,(0,255,255),2)
    except:
        pass
#     return center, radius        
#         cv2.circle(result,center,radius,(0,255,255),2)
#         cv2.circle(frame,center,radius,(0,255,255),2)
        

# Function to detect green buoys

def detect_green_buoy(i, frame):
    result = cv2.imread('result_green/result('+str(i)+').png')
    kernel = np.ones((2,2),np.uint8)
    kernel2 = np.ones((2,2),np.uint8)
    kernel3 = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(result,kernel2,iterations = 5)

    closing = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel3)
    # dilation = cv2.dilate(closing,kernel2,iterations = 15)

    thresh = cv2.cvtColor(dilation, cv2.COLOR_RGB2GRAY)

    _ , contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    try:
        cnts = sorted(contours, key = cv2.contourArea, reverse = True)
        area = cv2.contourArea(cnts[0])
        if area < 300 and area > 200:
            (x,y),radius = cv2.minEnclosingCircle(cnts[0])
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame,center,radius,(0,255,0),2)
    except:
        pass


# Combined Detection of buoys

def combined_detection():
    for i in range(0,200):
        frame = cv2.imread('Frames/'+str(i)+'.jpg',1)

        detect_orange_buoy(i, frame)
        detect_yellow_buoy(i, frame)
        detect_green_buoy(i, frame)

        cv2.imwrite('Output/combined/'+str(i)+'.png',frame)


# Video Creation
def create_video():
    img_list = []
    for i in range(0,200):
        img = cv2.imread('Output/combined/'+str(i)+'.png')
        img_list.append(img)
        
        out = cv2.VideoWriter('Output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, (img.shape[1],img.shape[0]))
        
        for i in range(len(img_list)):
            out.write(img_list[i])
            
    out.release()        

# call method for detection of buoys
combined_detection()

# create output video
create_video()
