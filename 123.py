import cv2
import pymurapi as mur
import time
import numpy as np

auv = mur.mur_init()
speed = 10
counter = 0

# функция определения знака числа
def zch(x): 
    if x==0: return 1 
    return (abs(x)/x)

# функция преведения скорости двигателей в работчий диапозон
def ogr(x): 
    if abs(x)>100: x=100*zch(x)
    return x

# функция движения по горизонтали
def y_drave(x): 
    x=ogr(x)
    auv.set_motor_power(1,x)
    auv.set_motor_power(2,x)

# функция движения по вертикали
def z_drave(x): 
    x=ogr(x)
    auv.set_motor_power(0,x)
    auv.set_motor_power(3,x)

# функция регулировки глубине в метрах
def kd(x): 
    z=auv.get_depth()-x
    z_drave((abs(z/3)**(1/3))*16*zch(z)*3)

def  Find_odject(image, name):
    
    iaverage = image.mean(axis=0).mean(axis=0)
    
    print(iaverage)
#    iaverage = (iaverage[2], iaverage[1], iaverage[0])
    auv.set_rgb_color(iaverage[2], iaverage[1], iaverage[0]) 
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
        
    # значеня настраиваются в зависимости от цвета
    hsv_low = (5, 100, 100)
    hsv_max = (150, 255, 255)

    mask = cv2.inRange(img, hsv_low, hsv_max)
    cnt, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(image, cnt, -1, (0,255,0), 2)

    

    # поиск координат центра найденной фигуры
    if cnt:
        try:
            # hull = cv2.convexHull(image)
            # approx = cv2.approxPolyDP(hull, cv2.arcLength(cnt, True), True)
            # ((x1, y1), (h, w), angele) = cv2.minAreaRect(approx)

            # print(x1, y1, h, w, angele)
            
            moments = cv2.moments(cnt[0])
            x = moments["m10"] / moments["m00"]
            y = moments['m01'] / moments['m00']


#            cv2. circle(image, (int(x), int(y)), 10, (0, 255, 0))
#
#            cv2.imshow(name, image)
#            cv2.waitKey(1)
            return x, y
        except ZeroDivisionError:
            return None


def search_2_line(img):
    if cor2: 
        x, y = cor2
        controlX = 2 * (x - width / 2) / width

        if abs(controlX) < 0.2:
            y_drave(15)

        elif controlX > 0.2:
            auv.set_motor_power(1,-speed)
            auv.set_motor_power(0,speed)
            
        elif controlX < -0.2:
            auv.set_motor_power(1,speed)
            auv.set_motor_power(0,-speed)
        else:
            y_drave(0)

#img = auv.get_image_front()
cap = cv2.VideoCapture(0)
         
while True:
    time.sleep(0)
#    if counter == 0:
#        kd(0.2)
#        counter = 10
#        
#    counter -= 1
#    img = auv.get_image_front()
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    
    print(height, width)
    print(Find_odject(frame, 'CCV2'))
    
    
    
    
    
    
    
