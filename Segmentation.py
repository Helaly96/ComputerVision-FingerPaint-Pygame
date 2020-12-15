import numpy as np 
import cv2 


class HandSegmentation():

    def ImageSegmentation(self,Image):
        if  self.ChoosenMethodOfSegmentation == "HSV":
            mask = cv2.inRange(Image, self.LowerHSV,self.UpperHSV)

        elif self.ChoosenMethodOfSegmentation == "InitialBackgroundSubtract":
            mask = Image

        return mask  

    def InitInitialBackgroundSegmentation(self):
        pass

    def Init_HSVSegmentation(self):
        self.LowerHSV=np.array([0, 10, 0])
        self.UpperHSV=np.array([88, 255, 255]) 

    def UpdateHSV(self,Val,UpdatedParam):
        print(Val)
        print(UpdatedParam)
        if UpdatedParam=="LH":
            self.LowerHSV[0]=Val
        elif UpdatedParam=="HH":
            self.UpperHSV[0]=Val
        elif UpdatedParam=="LS":
            self.LowerHSV[1]=Val
        elif UpdatedParam=="HS":
            self.UpperHSV[1]=Val
        elif UpdatedParam=="LV":
            self.LowerHSV[2]=Val
        elif UpdatedParam=="HV":
            self.UpperHSV[2]=Val


    def __init__(self,ChoosenMethodOfSegmentation):
        self.ChoosenMethodOfSegmentation= ChoosenMethodOfSegmentation
        if  ChoosenMethodOfSegmentation == "HSV":
            self.Init_HSVSegmentation()
        elif ChoosenMethodOfSegmentation == "InitialBackgroundSubtract":
            self.InitInitialBackgroundSegmentation()
         
