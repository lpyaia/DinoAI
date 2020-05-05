import cv2
import numpy as np
import os
import d3dshot
import time
import queue
from selenium import webdriver
from StopWatch import StopWatch
from operator import itemgetter
from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print(f"Key pressed: {k} - distX: {distX} - distY: {distY} - current speed: {currentSpeed}")

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

d = d3dshot.create(capture_output="numpy")
d.display = d.displays[0]

d.capture()

#browser = webdriver.Chrome("C:\\Users\\Lucas\\Documents\\Estudos\\Machine Learning\\DinoAI\\PythonDinoAI\\DinoAI\\DinoAI\\chromedriver.exe")
#browser.get("chrome://dino")

os.system('pause')

counter = 0
sumTime = 0
lastFrameDistX = 999999
frameSpeedCount = 0
dxArray = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
timerSpeedQueue = queue.Queue()
ableToMeasure = False
stopwatch = None
currentSpeed = 999999

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
            if x == 59 or w == 89:
                dino = [x, y, w, h]
                cv2.rectangle(img_crop, (x,y), (x+w,y+h), (0, 0, 0), 2)
        
            # Dinossauro abaixado
            elif w >= 127-5 and w <= 127+5 and h >= 58-5 and h <= 58+5:
                dino = [x, y, w, h]
                cv2.rectangle(img_crop, (x,y), (x+w,y+h), (0, 0, 0), 2)
            
            if x >= 148:
                # Passaro 1
                if w >= 97-5 and w <= 97+5 and h >= 70-5 and h <= 70+5:
                    passaro = [x, y, w, h]
                     
                # Passaro 2
                elif w >= 98-5 and w <= 98+5 and h >= 62-5 and h <= 62+5:
                    passaro = [x, y, w, h]
        
                elif w >= 15 and w <= 70 and h >= 50 and h <= 120:
                    cactos = [x, y, w, h]
                    obstaculos.append(cactos)
                    cactos = None

        if passaro != None:
            obstaculos.append(passaro)

        obstaculos.sort(key=lambda x: x[0])

        i = 0

        while i < len(obstaculos):
            j = i + 1
            
            dx = 9999

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

        if len(obstaculos) > 0:
            if obstaculos[0][0] > 1000 and ableToMeasure == False:
                ableToMeasure = True

            elif ableToMeasure == True and obstaculos[0][0] < 1000 and stopwatch is None:
                stopwatch = StopWatch()
                stopwatch.start()
                            
            elif obstaculos[0][0] < 400 and ableToMeasure == True:
                ableToMeasure = False
                stopwatch.stop()
                elapsedTime = stopwatch.get_elapsed_time()

                if elapsedTime < currentSpeed:
                    currentSpeed = elapsedTime
                    print(f"current speed: {currentSpeed}")

                stopwatch = None

        #for obstaculo in obstaculos[:]:
        #    cv2.rectangle(img_crop, (obstaculo[0] , obstaculo[1]), (obstaculo[0] + obstaculo[2], obstaculo[1] + obstaculo[3]), (0, 0, 0), 2)

        #cv2.imshow('Contours', img_crop)
        #cv2.waitKey(1)

        distX = 999999
        speed = 0
        distY = 999999

        if(len(obstaculos) > 0 and dino is not None):
            if frameSpeedCount > 0 and frameSpeedCount % 10 == 0:
                frameSpeedCount = 0
                #print(f"dxArray: {dxArray}")

            distX = obstaculos[0][0] - 148
            distY = dino[1] - obstaculos[0][1]

            if frameSpeedCount >= 0 and dxArray[frameSpeedCount - 1] != distX:
                dxArray[frameSpeedCount] = distX
                frameSpeedCount += 1

        tEnd = time.perf_counter()

        #print(f"Dino {dino}")
        #print(f"distX: {distX} - distY: {distY} - speed: {speed}")

        sumTime += (tEnd - tInit) * 1000
        counter += 1

        if(counter >= 100):
            averageTime = sumTime / counter
            sumTime = 0
            counter = 0

            #print(f"Average Time after 100 frames: {averageTime:0.2f} ms")

listener.join()  # remove if main thread is polling self.keys