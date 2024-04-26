import cv2
import pymurapi as mur
import time
import numpy as np

auv = mur.mur_init()
speed = 10
counter = 0

k = 0.4
is_right =False
is_left =False


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
    auv.set_motor_power(2,x-7.5)

# функция движения по вертикали
def z_drave(x): 
    x=ogr(x)
    k = 15
   
    auv.set_motor_power(3,x + k)    
    auv.set_motor_power(0,x)

# функция регулировки глубине в метрах
def kd(x): 
    z=auv.get_depth()-x
    z_drave((abs(z/3)**(1/3))*16*zch(z)*3)

# Функция для поиска линии в поле зрения камеры
def  Find_odject(image, name):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

    # значеня настраиваются в зависимости от цвета
    hsv_low = (70, 85, 85)
    hsv_max = (160, 210, 210)

    mask = cv2.inRange(img, hsv_low, hsv_max)
    cnt, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    try:   
        moments = cv2.moments(cnt[0])
        x = moments["m10"] / moments["m00"]
        y = moments['m01'] / moments['m00']

#        pt1 = int(width//2 + width * (k/2))
#        pt2 = int(width//2 - width * (k/2))
#
#        cv2.circle(image, (int(x), int(y)), 5, (255, 0, 0))
#        cv2.rectangle(image,(pt1,height),(pt2,0),(0,255,0),2)
#        cv2.line(image,(0,height//2),(width,height//2),(0,0,255),2)
#        cv2.line(image,(width//2,0),(width//2,height),(0,0,255),2)


#        cv2.imshow(name, image)
#        cv2.waitKey(1)
        return x, y
    
    except ZeroDivisionError:
        return None
    except IndexError:
        return None

# Функция выравнивания робота по центру относительно 2/3 изображения
def search_2_line(cor2):
    if cor2: 
        x, _ = cor2
        controlX = 2 * (x - width / 2) / width
        
        if abs(controlX) < k:
            print('controlX:', controlX)
            y_drave(20)

        elif controlX > k and not is_left:
            auv.set_motor_power(1,-speed)
            auv.set_motor_power(2,speed)
            
        elif controlX < -k and not is_right:
            auv.set_motor_power(1,speed)
            auv.set_motor_power(2,-speed)

        else:
            y_drave(15)

# Blue BGR 150 145 20
# Red BGR 125 100 185
# Yellow BGR 70 139 95

# Функция выравнивания робота по центру относительно 1/3 изображения
def search_1_line(cor1, cor2):
    if cor1: 
        x, _ = cor1
        controlX = 2 * (x - width / 2) / width

        if abs(controlX) < 0.05:
            is_left = False
            is_right = False
            search_2_line(cor2)

        elif abs(controlX) < k:
            search_2_line(cor2)

        elif controlX > k:
            is_right = True
            auv.set_motor_power(1,-speed)
            auv.set_motor_power(2, speed)
            
        elif controlX < -k:
            is_left = True
            auv.set_motor_power(1,speed)
            auv.set_motor_power(2,-speed)

        else:
            y_drave(10)

            
# Функция удержания заданной высоты 
def dive(z=0.5):
    global counter
    if counter == 0:
        kd(z)
        counter = 10
    counter -= 1
    
cap = cv2.VideoCapture(1)

while True:
    time.sleep(0.1)
#    dive()

    ret, image = cap.read()
    
    
    
    time.sleep(4)
    auv.set_motor_power(0,-x)
    auv.set_motor_power(3,-x - k) 
    time.sleep(6)
    break

#height, width = image.shape[:2]
#    
#    img1 = image[:height//3, 0:width]
            #    # img2 = image[height//3:height, 0:width]
#    img2 = image[height//3:height//3*2, :]
#
#
#    cor1 = Find_odject(img1, 'CCV1')
#    cor2 = Find_odject(img2, 'CCV2')
##    timee()
#    print('cor1',cor1)
#    print('cor2',cor2)
#    search_1_line(cor1, cor2)
    
    
    
    
    
    
