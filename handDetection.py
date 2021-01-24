import cv2;
import numpy as np;
import math
from threading import Thread

class handDetector():
    def findContours(self,mask):
            #find contours
        contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #find contour of max area(hand)
        contours = max(contours, key = lambda x: cv2.contourArea(x))
        return contours

    def getApprox(self, contours):
        #approx the contour a little
        epsilon = 0.0005*cv2.arcLength(contours,True)
        approx= cv2.approxPolyDP(contours,epsilon,True)
        return approx;
        
    def findCovexHull(self,contours, approx):
        #make convex hull around hand
        hull = cv2.convexHull(contours)
        
        #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(contours)
      
        #find the percentage of area not covered by hand in convex hull
        self.arearatio=((areahull-areacnt)/areacnt)*100
    
        #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        return cv2.convexityDefects(approx, hull)
        
        # l = no. of defects
    def findingFinger(self,defects,approx):
        fingers=0
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            #distance between point and convex hull
            d=(2*ar)/a
            
            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                
            
            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            if angle <= 90 and d>30:
                fingers += 1
                #cv2.circle(self.roiLeft, far, 3, [255,0,0], -1)
                #cv2.circle(self.roiRight, far, 3, [255,0,0], -1)

        
            #draw lines around hand
            #cv2.line(self.roi,start, end, [0,255,0], 2)
        return fingers;

    def getResultDetection(self, leftFingers, rightFingers):
        leftHandOpen = False;
        rightHandOpen = False;

        leftFingers+=1
        if leftFingers>=3:
            leftHandOpen = True;
        
        #right text
        rightFingers+=1
        if rightFingers>=3:
            rightHandOpen = True;
        
        if leftHandOpen & rightHandOpen:
            return "STRAIGHT"
        elif leftHandOpen:
            return "RIGHT"
        elif rightHandOpen:
            return "LEFT"
        else:
            return "STRAIGHT"

    def startHandDetection(self, frame):
        self.frame = frame;
        
        #creating a roi for both hands
        self.roiLeft = self.frame[self.leftBox.startY:self.leftBox.endY, self.leftBox.startX:self.leftBox.endX]
        self.roiRight = self.frame[self.rightBox.startY:self.rightBox.endY, self.rightBox.startX:self.rightBox.endX]

        #setting the kernal
        self.kernel = np.ones((3,3),np.uint8)

        #fill dark sport in the hand to make it easier to get the contours
        self.maskLeftHand = self.roiLeft;
        self.maskRightHand = self.roiRight;

        # find the countours in the hand
        contoursLeftHand = self.findContours(self.maskLeftHand);
        contoursRightHand = self.findContours(self.maskRightHand);

        approxLeftHand = self.getApprox(contoursLeftHand);
        approxRightHand = self.getApprox(contoursRightHand);

        #finding the convex hull for
        defectsLeft = self.findCovexHull(contoursLeftHand,approxLeftHand)
        defectsRight = self.findCovexHull(contoursRightHand,approxRightHand)

        # checking how many fingers are up
        leftFingers = self.findingFinger(defectsLeft, approxLeftHand)
        rightFingers = self.findingFinger(defectsRight, approxRightHand)

        return self.getResultDetection(leftFingers,rightFingers);

    def __init__(self):
        self.leftBox = handBox(0,0,250,250)
        self.rightBox = handBox(400,0,250,650)

class handBox:
    def __init__ (self, startX, startY, endY, endX):
        self.startX = startX
        self.startY = startY
        self.endY = endY
        self.endX = endX