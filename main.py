# Imports
#########
import cv2  as cv
import numpy as np
from Segmentation import HandSegmentation
import ImageOperation
import time 
from Helpers import *
##############################################
# Configuration
###############
# "InitialBackgroundSubtract" or "HSV"
ChoosenMethodOfSegmentation="HSV"
SliderMaxValue=255

#Default params
LowerH_SliderValue= 0
HigherH_SliderValue= 185

LowerS_SliderValue= 0
HigherS_SliderValue= 255

LowerV_SliderValue= 81
HigherV_SliderValue= 255

WindowTitle= "MainApplication"


###############################################
# Inits
#######
capture= cv.VideoCapture(0)
SegmentationObject= HandSegmentation(ChoosenMethodOfSegmentation)
capture= ImageOperation.make_720p(capture)
#points that are drawn by the user
ListToDraw= []
#Slider that will hold the info needed for HSV Filteration.
cv.namedWindow(WindowTitle)
cv.createTrackbar("LowerHValue", WindowTitle , SegmentationObject.LowerHSV[0], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"LH") )
cv.createTrackbar("LowerSValue", WindowTitle , SegmentationObject.LowerHSV[1], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"LS"))
cv.createTrackbar("LowerVValue", WindowTitle , SegmentationObject.LowerHSV[2], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"LV"))
cv.createTrackbar("UpperHValue", WindowTitle , SegmentationObject.UpperHSV[0], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"HH"))
cv.createTrackbar("UpperSValue", WindowTitle , SegmentationObject.UpperHSV[1], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"HS"))
cv.createTrackbar("UpperVValue", WindowTitle , SegmentationObject.UpperHSV[2], SliderMaxValue, lambda x: SegmentationObject.UpdateHSV(x,"HV"))

# Time before the loop Starts.
TimerStart=time.time()

# Secounds to wait before the drawing begins
NeededTimeToStart= 3

###############################################
while True:
    # Time at the start of the loop
    CurrentTime= time.time()
    # Passed Time From the start 
    TimePassed= CurrentTime - TimerStart
    # Read frame from the video stream
    ret, frame = capture.read()
    if frame is None:
        break
    # Mirror the frame
    frame = cv.flip(frame,1)
    # Draw  the ROI where the canvas will be drawn on it.
    image = cv.rectangle(frame, (50,50), (500,550), (255,255,255), 3)

    # Time Remaining before drawing begins
    RemainingTime= NeededTimeToStart - TimePassed
    # Check if it's the time to draw
    if RemainingTime>0:      
        cv.putText(image,"Secounds Remaining is "+str(RemainingTime) ,(600,10), cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
    else:
        # ... Add the logic for the old image ...
        mask= SegmentationObject.ImageSegmentation(image[50:550,50:500])
        # Thresholding the imgae 
        _,roi = cv.threshold(mask,40,255,cv.THRESH_BINARY)
        #Dilation to close the gaps?
        kernel = np.ones((3,3),np.uint8)
        roi = cv.dilate(mask,kernel,iterations =1)
        # add the ROI for better visualization
        contours, _ = cv.findContours(roi, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # Check if there is a contour
        if len(contours)>0:
            # Get the biggest contour
            BiggestContour = max(contours, key=cv.contourArea)
            # the offset in x and y
            BiggestContour+=50
            try:
                # Get the convex hull of the biggest contour
                hull = cv.convexHull(BiggestContour,returnPoints = False)      
            except:
                hull = []
            # Get the perimtere? of the biggest contour
            perimeter = cv.arcLength(BiggestContour,True)
            # Points that represent the two top of fingers
            ClearPoints= []
            # Condition on the countour param
            if perimeter>300:
                # Draw the hand contour
                cv.drawContours(frame, [BiggestContour], 0, (0,255,0), 3)
                j= 0
                for i in range(len(hull)-1):
                    if XDifferenceBetweenTwoPoints(BiggestContour[hull[j]][0][0],BiggestContour[hull[j+1]][0][0])>= 10:
                        ClearPoints.append(BiggestContour[hull[j]][0][0])  
                    j+=1 
                ClearPoints.sort(key= YAxis)
                ClearPoints=ClearPoints[0:2]
                for ClearPointsCounter in range(len(ClearPoints)):
                    cv.circle(frame,tuple(ClearPoints[ClearPointsCounter]),6,[255,255,255],-1) 
                if (len(ClearPoints)>=2):
                    if (XDifferenceBetweenTwoPoints(ClearPoints[0],ClearPoints[1])<150):
                        ClearPoints.sort(key=XAxis)
                        ListToDraw.append(ClearPoints[0])
                    else:
                        ListToDraw=[]
                else:
                    ListToDraw=[]

        frame[50:550,50:500]= cv.bitwise_and(frame[50:550,50:500],frame[50:550,50:500],mask=roi)

    for i in range(len(ListToDraw)):
        if not(i==0):
            p= ListToDraw[i]
            new_x=p[0]+600
            cv.circle(frame, (new_x,p[1]), 20, (255, 0, 0), -1)
    cv.imshow("Frame", frame)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break