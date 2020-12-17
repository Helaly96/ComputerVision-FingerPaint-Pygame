# Required Imports to run the project
import numpy as np
import cv2 
import FingerDrawing
import time


def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def XDifferenceBetweenTwoPoints(P1,P2):
    return abs(P1[0]-P2[0])

def YAxis(Element):
    return Element[1]

def XAxis(Element):
    return Element[0]

#Capture the Camera stream
cap = cv2.VideoCapture(0)
make_720p()

TimerStart=time.time()
NeededTimeToStart= 3

#Reigon of image that will hold the pixel values that will be deleted
OldReigonOfImage=[]
ListToDraw=[]
while(True):

    CurrentTime=time.time()
    difference= CurrentTime - TimerStart

    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    #Image with the ROI where the canvas will be drawn on it.
    image = cv2.rectangle(frame, (50,50), (500,550), (255,255,255), 3)

    RemainingTime= NeededTimeToStart - difference
    if RemainingTime>0:      
        cv2.putText(image,"Secounds Remaining is "+str(RemainingTime) ,(600,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
        cv2.imshow('frame',frame)
    else:
        if len(OldReigonOfImage)==0:
            OldReigonOfImage= image[50:550,50:500]
            OldReigonOfImage= cv2.cvtColor(OldReigonOfImage,cv2.COLOR_BGR2GRAY)
        else: 
            GreyedReigonImage= cv2.cvtColor(image[50:550,50:500],cv2.COLOR_BGR2GRAY)
            roi = cv2.bitwise_xor(GreyedReigonImage,OldReigonOfImage,mask = OldReigonOfImage)
            ret3,roi = cv2.threshold(roi,40,255,cv2.THRESH_BINARY)
            #kernel = np.ones((5,5),np.uint8)
            #roi = cv2.erode(roi,kernel,iterations =1)
            
            cv2.imwrite("test.png",roi)
            # find the contours from the thresholded image
            contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours)>0:
                c = max(contours, key=cv2.contourArea)
                c+=50
                try:
                    # needs to be false to be able to find the hull defects
                    hull = cv2.convexHull(c,returnPoints = False)    
                    hull_ = cv2.convexHull(c,returnPoints = True)    
                except:
                    hull = []

                perimeter = cv2.arcLength(c,True)
                if perimeter>300:
                    image[50:550,50:500]= cv2.bitwise_and(image[50:550,50:500],image[50:550,50:500],mask=roi)
                    
                    cv2.drawContours(image, [c], 0, (0,255,0), 3)
                    cv2.drawContours(image, [hull_], 0, (255,0,0), 3)
                    
                    epsilon = 0.1*cv2.arcLength(hull_,True)
                    approx = cv2.approxPolyDP(hull_,epsilon,True)
                    
                    print(len(approx))
                    for p in approx:
                        cv2.circle(image,tuple(p[0]),5,[0,255,0],-1)

                    j=0
                    ClearPoints=[]
                    for i in range(len(hull)-1):
                        
                        if XDifferenceBetweenTwoPoints(c[hull[j]][0][0],c[hull[j+1]][0][0])>= 7:
                            ClearPoints.append(c[hull[j]][0][0]) 
                            #cv2.circle(image,tuple(c[hull[j]][0][0]),5,[255,255,255],-1)  
                        j+=1 
                    ClearPoints.sort(key= YAxis)
                    ClearPoints=ClearPoints[0:2]

                    if (len(ClearPoints)>=2):
                        if (XDifferenceBetweenTwoPoints(ClearPoints[0],ClearPoints[1])<150):
                            ClearPoints.sort(key=XAxis)
                            ListToDraw.append(ClearPoints[0])
                        else:
                            ListToDraw=[]
                    else:
                        ListToDraw=[]

            else:
                image[50:550,50:500]= cv2.bitwise_and(image[50:550,50:500],image[50:550,50:500],mask=roi)
                ListToDraw=[]
                
            # cv2.imshow('roi',roi)
        for i in range(len(ListToDraw)):
            p= ListToDraw[i]
            new_x=p[0]+600
            cv2.circle(image, (new_x,p[1]), 8, (255, 0, 0), -1)
        
        cv2.putText(image,"Draw!" ,(650,10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        cv2.imshow('frame',image)
        

    # Display the resulting frame
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
