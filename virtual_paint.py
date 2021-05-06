import cv2
import numpy as np

# Web-Camera 

# capture from camera
cap = cv2.VideoCapture(0)
# setting width of frame
cap.set(3,1024)
# setting height of frame
cap.set(4,1024)
# Exposure time
cap.set(10,1024)



# Colour list for Orange, purple, green in order hmin,smin,vmin,hmax,smax,vmax
myColour = [[0,159,118,19,255,255],
             [105,41,35,137,255,255],
             [44,80,23,69,255,255]]

# Colour list for corresponding pen colour -- Orange, Purple, Green in BGR format
myColourValues = [[0,128,255],
                 [102,0,51],
                 [0,204,0]]

# List of points
myPoints = []     # [x, y, colorID]  


# Function to find colour  
# For loop to obtain all three colours -- Orange, Purple, Green from list
# '0' inclusive, '3' exclusive
def findColour(img, myColour,myColourValues):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColour:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imghsv, lower, upper)
        x,y = getContour(mask)
        cv2.circle(img_copy,(x,y),10,myColourValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints

        # cv2.imshow(str(color[0]),mask)

# Function to get bounding box
def getContour(img):
    contours,hierrachy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area> 500:
            # cv2.drawContours(img_copy,contours,-1,(0,0,255),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawCanvas(myPoints,myColourValues):
    for points in myPoints:
        cv2.circle(img_copy,(points[0],points[1]),10,myColourValues[points[2]],cv2.FILLED)


while True:
    success, img = cap.read()
    img_copy = img.copy()
    newPoints = findColour(img, myColour,myColourValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawCanvas(myPoints, myColourValues)
    cv2.imshow("Result",img_copy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

