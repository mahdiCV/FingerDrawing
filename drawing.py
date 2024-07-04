import numpy as np
import cv2 
import imutils

import mediapipe as mp

from save_drawing import save_draw

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)

black = (0,0,0)         # Black     - b/B
white = (255,255,255)   # White     - w/W
blue = (255,0,0)        # Blue      - b/B
green = (0,255,0)       # Green     - g/G
red = (0,0,255)

colors = {1:[white, 'w/W', 'white'], 2:[blue, 'b/B', 'blue'], 3:[green, 'g/G', 'green'], 4:[red, 'r/R', 'red']}

def coloring(diction, window,font, text_color):
    width = 64
    sx, sy = 0, width
    for i in diction.keys():
        cv2.rectangle(window, (sx, 0), (sx+width, sy), diction[i][0], 2)
        cv2.putText(window, diction[i][1], (sx+15, int(sy/2)+5), font, 0.5, text_color, 2)
        sx += width

color = white

pts = []

canvas = None
cx, cy = "", ""

message = "white"
message_color = white

timestamp = 0


while capture.isOpened():
        _, image = capture.read()
        
        h, w, c = image.shape
        width = 64

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  

        font = cv2.FONT_HERSHEY_COMPLEX

        cv2.putText(image, 'ALL', (w-45, h-30), font, .5, white, 2)
        cv2.putText(image, '[-1]', (w-112, h-30), font, .5, white, 2)
        cv2.putText(image, 'Delete:', (w-210, h-28), font, .7, white, 2)

        cv2.putText(image, 'SAVE', (20, h-38), font, .7, white, 2)
        cv2.putText(image, 'or press s/S', (15, 470), font, 0.6, white, 1)
        cv2.rectangle(image, (15,420), (85,450), white, 2)

        cv2.putText(image, "Color: ", (10,140), font, .6, black, 2)
        cv2.rectangle(image, (80, 125), (100, 145), message_color, -1)
        cv2.putText(image, message, (110, 140), font, .6, black, 2)

        for i in colors.keys():
            coloring(colors, image, font, black)

        if canvas is None:
            canvas = np.zeros_like(image)
  

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                #h, w, c = image.shape
                cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                center = (cx, cy)
                #print(center)
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

            cv2.putText(image, 'Drawing...', (10,100), font, 0.7, 2)
            
                                    
            if cy > h-60 and cy< h-10:
                if cx > w -125 and cx < w-75:
                    canvas = np.zeros((h-64,w,3))
                    pts = pts[:-1]
                    print('Clearing last line segment, pts:', pts)
                elif cx > w-55 and cx < w-5:
                    canvas = np.zeros_like((h-64,w,3))
                    pts = []
                    print('Clearing entire canvas, pts:', pts)

            if 20 < cx < 650 and 15 <= cy <= 600:
                pts.append(center)
                print('Adding point to pts:', pts)


            if cy > 0 and cy < 64:
                for i in range(len(colors)):
                    if cx > i*64 and cx < (i+1)*64:
                        color = colors[i+1][0]
                        message_color = colors[i+1][0]
                        message = colors[i+1][2]
                        print('Changing color to', message)

                    else:
                        continue
            if 420 < cy < 450 and 15 < cx < 85:
                save_draw(canvas)

        else:
            cv2.putText(image, 'No drawing', (10,100), font, 0.7, black,2)                
            pts = []

        for i in range(1, len(pts)):
            if len(pts) > 2:
                cv2.line(canvas, pts[i-1], pts[i], color, 4)
                cv2.line(image, pts[i-1], pts[i], color, 4)
            else:
                continue



        cv2.imshow('image', image)
        cv2.imshow('Canvas', canvas)

        key = cv2.waitKey(1)
        if key == 27:
            break


        for i in colors.keys():
            keyword = colors[i][1]
            if key == ord(keyword.split('/')[0]) or key == ord(keyword.split('/')[1]):
                color = colors[i][0]

                message = colors[i][2]
                message_color = colors[i][0]
            elif key==ord('S') or key==ord('s'):
                save_draw(canvas)

capture.release()
cv2.destroyAllWindows()




        


    

