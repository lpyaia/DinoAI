import cv2
import numpy as np
import os
from operator import itemgetter
import d3dshot
import time

path = 'C:\\Users\\Lucas\\Documents\\Estudos\\Machine Learning\\DinoAI\\Cenario-Novo\\'
files = os.listdir('C:\\Users\\Lucas\\Documents\\Estudos\\Machine Learning\\DinoAI\\Cenario-Novo\\')

d = d3dshot.create(capture_output="numpy")
d.display = d.displays[0]

d.capture()

os.system('pause')

counter = 0
sumTime = 0

while(True):
    tInit = time.perf_counter()

    imgArray = d.get_latest_frame()

    if(imgArray is not None):
        imgArray = d.get_latest_frame()
        img_crop = imgArray[200:200+315, 1:1+1365]
        img_crop = cv2.cvtColor(img_crop, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(img_crop, (5,5), 0)
        ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)

        contours =  cv2.findContours(thresh_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]

        obstaculos = list()
        dino = None;
        cactos = None;
        passaro = None;

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)

            # Dinossauro
            if w >= 87-5 and w <= 98+5 and h >= 95-5 and h <= 105+5:
                dino = [x, y, w, h]
                cv2.rectangle(img_crop, (x,y), (x+w,y+h), (0, 0, 0), 2)
        
            # Dinossauro abaixado
            elif w >= 127-5 and w <= 127+5 and h >= 58-5 and h <= 58+5:
                dino = [x, y, w, h]
                cv2.rectangle(img_crop, (x,y), (x+w,y+h), (0, 0, 0), 2)

            # Passaro 1
            elif w >= 97-5 and w <= 97+5 and h >= 70-5 and h <= 70+5:
                passaro = [x, y, w, h]

            # Passaro 2
            elif w >= 98-5 and w <= 98+5 and h >= 62-5 and h <= 62+5:
                passaro = [x, y, w, h]
        
            elif w >= 15 and w <= 70 and h >= 50 and h <= 120:
                cactos = [x, y, w, h]
        
            if cactos != None:
                obstaculos.append(cactos)
                cactos = None

        obstaculos.sort(key=lambda x: x[0])

        i = 0
        while i < len(obstaculos):
            j = i + 1

            if j < len(obstaculos):
                dX = obstaculos[j][0] - obstaculos[i][0] - obstaculos[i][2]

                if dX <= 10:
                    if obstaculos[j][1] < obstaculos[i][1]:
                        obstaculos[i][1] = obstaculos[j][1]
                        obstaculos[i][3] = obstaculos[j][3]

                    obstaculos[i][2] = obstaculos[j][2] + obstaculos[i][2] + dX
            
                    obstaculos.remove(obstaculos[j])
                    i -= 1
            i += 1

        if passaro != None:
            obstaculos.append(passaro)

        #for obstaculo in obstaculos[:]:
        #    cv2.rectangle(img_crop, (obstaculo[0] , obstaculo[1]), (obstaculo[0] + obstaculo[2], obstaculo[1] + obstaculo[3]), (0, 0, 0), 2)

        #cv2.imshow('Contours', img_crop)
        #cv2.waitKey(1)

        tEnd = time.perf_counter()

        sumTime += (tEnd - tInit) * 1000
        counter += 1

        if(counter >= 100):
            averageTime = sumTime / counter
            sumTime = 0
            counter = 0

            print(f"Average Time after 100 frames: {averageTime:0.2f} ms")