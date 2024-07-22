import numpy as np
import cv2 

from HandModule import handDetector

class VideoCapture:
    """
    Capture Video frame 
    """
    def __init__(self, camera_index=0):
        """
        Initialize a window of capturing camera, 
        Set the frame width to 1280 pixels and the frame height to 720 pixels
        """
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(3, 1280)
        self.capture.set(4, 720)
    
    def read(self):
        return self.capture.read()

class HandDetector:
    def __init__(self):
        self.detector = handDetector()

    def findHands(self, image):
        return self.detector.findHands(image)

    def findPosition(self, hands, draw=False):
        return self.detector.findPosition(hands, draw)
    
    def fingerUp(self):
        return self.detector.fingerUp()

class DrawingCanvas:
    """
    Represent the canvas functionality
    """
    def __init__(self, width=1280, height=720):
        """
        Initialize the height and width of the canvas

        :param width: The width of the canvas (default is 1280).
        :param height: The height of the canvas (default is 720).
        """
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.drawColor = (255, 0, 255)
        self.brushThickness = 10
        self.eraserThickness = 50
        self.xp, self.yp = 0, 0

    def drawLine(self, x1, y1, x2, y2, color, thickness):
        """
        Drawing line between two points on the canvas 

        :param x1: The x-coordinate of the starting point.
        :param y1: The y-coordinate of the starting point.
        :param x2: The x-coordinate of the ending point.
        :param y2: The y-coordinate of the ending point.
        :param color: The color of the line.
        :param thickness: The thickness of the line.
        """
        cv2.line(self.canvas, (x1, y1), (x2, y2), color, thickness)

    def updateCanvas(self, image):
        """
        Updates the canvas and merges it with the input image.
        
        :param image: The input image to merge with the canvas.
        :return: The merged image.
        """
        imgGray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv ,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(image, imgInv)
        img = cv2.bitwise_or(img, self.canvas)
        return img
    

class ColorSelection:
    """
    A class to function color selecting 
    """
    def __init__(self, colors, positions):
        """
        Initializes the color selection 

        :param colors: A list of colors available for selection.
        :param positions: A list of positions where the colors are displayed.
        """
        self.colors = colors
        self.positions = positions

    def drawPalette(self, image):
        """
        Draw color palette on the given canvas

        :param image: The input image where the palette is to be drawn.
        """
        for i, color in enumerate(self.colors):
            cv2.rectangle(image, (self.positions[i][0], self.positions[i][1],
                        self.positions[i][2], self.positions[i][3]), color, 3)
            
    def selectColor(self, x, y):
        """
         Selects a color from the palette based on the given coordinates.
        
        :param x: The x-coordinate of the selection point.
        :param y: The y-coordinate of the selection point.
        :return: The selected color, or None if no color is selected.
        """
        for i, pos in enumerate(self.positions):
            if pos[0] < x < pos[0] + 140 and pos[1] < y < pos[1] + 100:
                return self.colors[i]
        return None



def main():
    video_capture = VideoCapture()
    hand_detector = HandDetector()
    drawing_canvas = DrawingCanvas()
    color_selections = ColorSelection(colors=[(0, 0, 255), (255, 0, 255), (0, 255, 255), (0, 0, 0)],
                                     positions=[(40, 1, 140, 100), (320, 1, 140, 100), (570, 1, 140, 100), (1090, 1, 140, 100)])


    while True:
        success, image = video_capture.read()
        if not success:
            break
        image = cv2.flip(image, 1)

        hands = hand_detector.findHands(image)
        landmarks = hand_detector.findPosition(hands, draw=False)

        color_selections.drawPalette(image)


        if len(landmarks) != 0: 
            
            x1, y1 = landmarks[8][1:]
            x2, y2 = landmarks[12][1:]

            fingers = hand_detector.fingerUp()

            #selection mode
            if fingers[1] and fingers[2]:
                drawing_canvas.xp, drawing_canvas.yp = 0, 0
                if y1 < 125:
                    selected_color = color_selections.selectColor(x1, y1)
                    if selected_color is not None:
                        drawing_canvas.drawColor = selected_color
                                        
                cv2.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), drawing_canvas.drawColor, cv2.FILLED)

            # drawing mode
            if fingers[1] and not fingers[2]:

                if drawing_canvas.xp == 0 and drawing_canvas.yp == 0:
                    drawing_canvas.xp, drawing_canvas.yp = x1, y1
                    
                if drawing_canvas.drawColor == (0, 0, 0):
                    drawing_canvas.drawLine(drawing_canvas.xp, drawing_canvas.yp, x1, y1, drawing_canvas.drawColor, drawing_canvas.eraserThickness)
                
                else:
                    drawing_canvas.drawLine(drawing_canvas.xp, drawing_canvas.yp, x1, y1, drawing_canvas.drawColor, drawing_canvas.brushThickness)
                    
                drawing_canvas.xp, drawing_canvas.yp = x1, y1


        image = drawing_canvas.updateCanvas(image)

        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()