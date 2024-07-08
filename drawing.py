import numpy as np
import cv2 
import os

from HandModule import handDetector

capture = cv2.VideoCapture(0)

capture.set(3, 1280)
capture.set(4, 720)

detector = handDetector()

brushThickness = 25
eraserThickness = 100

folderPath = 'Header'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (255, 0, 255)

xp, yp = 0, 0
imageCanvas = np.zeros((720, 1280, 3), np.uint8)

while capture.isOpened():
    _, image = capture.read()
    image = cv2.flip(image, 1)

    hands = detector.findHands(image)
    landmarks = detector.findPosition(hands, draw=False)
    
    if len(landmarks) != 0:
        x1, y1 = landmarks[8][1:]
        x2, y2 = landmarks[12][1:]

        fingers = detector.fingerUp()


        #selection mode
        if fingers[1] and fingers[2]:
            xp, yp = 0
            if y1 < 125:
                if 250 < x1 < 450:
                    pass
                elif 550 < x1 < 750:
                    pass
                elif 800 < x1 < 950:
                    pass
                elif 1050 < x1 < 1200:
                    pass
            
            cv2.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # drawing mode
        if fingers[1] and fingers[2] == False:
            # print('drawing mode')
            cv2.circle(image, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp==0 and yp==0:
                xp, yp = x1, y1

            cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)


            if drawColor == (0, 0, 0):
                cv2.line(image, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


    imgGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imageCanvas)

    cv2.imshow('image', hands)
    cv2.waitKey(1)
       

capture.release()
cv2.destroyAllWindows()




        


    

