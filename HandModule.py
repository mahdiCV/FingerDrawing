import cv2
import mediapipe as mp

class handDetector():

    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        
        self.mpDraw = mp.solutions.drawing_utils
        self.tipId = [4, 8, 12, 16, 20]
    
    def findHands(self, img, draw=True):
        img  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img)

        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmark, self.mpHands.HAND_CONNECTIONS)
        return img
        

    def findPosition(self, img, handNo=0, draw=True):
        self.landmarks = []        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmarks.append([idx, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return self.landmarks

    def fingerUp(self):

        fingers = []
        if self.landmarks[self.tipId[0]][1] > self.landmarks[self.tipId[0] -1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for idx in range(1, 5):
            if self.landmarks[self.tipId[idx]][2] < self.landmarks[self.tipId[idx] -2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers