import os 
from datetime import datetime
import cv2

data_time = datetime.now().strftime("%d-%m-%y_%H:%M")

dir_name = 'Drawings'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

number_of_drawings = len([drawings for drawings in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, drawings))])

new_drawing = 'drawing' + str(number_of_drawings+1) + '_' + data_time + '.jpg'

def save_draw(image):
    cv2.imwrite(dir_name + '/' + new_drawing, image)