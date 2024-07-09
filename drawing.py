import numpy as np
import cv2 

from HandModule import handDetector

capture = cv2.VideoCapture(0)

capture.set(3, 1280)
capture.set(4, 720)

detector = handDetector()

brushThickness = 15
eraserThickness = 100

# Define the colors and their positions
colors = [(0, 0, 255), (255, 0, 255), (0, 255, 255), (0,0,0)] 
color_positions = [(40, 1, 140, 100), (320, 1, 140,100), (570, 1, 140, 100), (1090, 1, 140, 100)]

drawColor = (255, 0, 255)
eraserColor = (0, 0, 0)

xp, yp = 0, 0
imageCanvas = np.zeros((720, 1280, 3), np.uint8)

while capture.isOpened():
    _, image = capture.read()
    image = cv2.flip(image, 1)

    hands = detector.findHands(image)
    landmarks = detector.findPosition(hands, draw=False)
    for i, color in enumerate(colors):
        cv2.rectangle(image, (color_positions[i][0], color_positions[i][1],
                        color_positions[i][2], color_positions[i][3]), color, 3)

    if len(landmarks) != 0: 
        # xp, yp = 0, 0
        x1, y1 = landmarks[8][1:]
        x2, y2 = landmarks[12][1:]

        fingers = detector.fingerUp()

        #selection mode
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0 
            if y1 < 125:
                for i, pos in enumerate(color_positions):
                    if pos[0] < x1 < pos[0] + 140:
                        drawColor = colors[i]
                                    
            cv2.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # drawing mode
        if fingers[1] and not fingers[2]:

            if xp == 0 and yp == 0:
                xp, yp = x1, y1
                
            if drawColor == eraserColor:
                cv2.line(image, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(image, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                
            xp, yp = x1, y1


    imgGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv ,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(image, imgInv)
    img = cv2.bitwise_or(img, imageCanvas)

    cv2.imshow('image', img)
    cv2.waitKey(1)
       

capture.release()
cv2.destroyAllWindows()