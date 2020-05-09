import cv2
import numpy as np
import d3dshot
from StopWatch import StopWatch

class Vision:

    def __init__(self, display):
        self.__d = d3dshot.create(capture_output="numpy")
        self.__d.displays[display]
        self.__dx = 999999
        self.__dy = 999999
        self.__speed = 0
        self.__dt = 999999
        self.__ableToMeasure = False
        self.__stopwatch = None
        self.__dino = None;
        self.__initCaptureScreen()

    def __initCaptureScreen(self):
        if self.__d is not None:
            self.__d.capture()
        else:
            print('capturing screen error!')

    def __getLastestFrame(self):
        return self.__d.get_latest_frame()

    def __findImageContours(self, image):
        imgCrop = image[200:200+315, 1:1+1365]
        imgCrop = cv2.cvtColor(imgCrop, cv2.COLOR_RGB2GRAY)

        blur = cv2.GaussianBlur(imgCrop, (5,5), 0)
        ret, threshImg = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)
        contours = cv2.findContours(threshImg, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]

        return contours, imgCrop

    def __getEnemiesFromContours(self, contours):
        enemies = list()
        cactos = None;
        passaro = None;

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)

            # Dinossauro
            if x == 59 or w == 89:
                self.__dino = [x, y, w, h]
        
            # Dinossauro abaixado
            elif w >= 127-5 and w <= 127+5 and h >= 58-5 and h <= 58+5:
                self.__dino = [x, y, w, h]
            
            if x >= 148:
                # Passaro 1
                if w >= 97-5 and w <= 97+5 and h >= 70-5 and h <= 70+5:
                    passaro = [x, y, w, h]
                     
                # Passaro 2
                elif w >= 98-5 and w <= 98+5 and h >= 62-5 and h <= 62+5:
                    passaro = [x, y, w, h]
        
                elif w >= 15 and w <= 70 and h >= 50 and h <= 120:
                    cactos = [x, y, w, h]
                    enemies.append(cactos)
                    cactos = None

        if passaro != None:
            enemies.append(passaro)

        enemies.sort(key=lambda x: x[0])

        return enemies

    def __groupClosestEnemies(self, enemies):
        i = 0

        while i < len(enemies):
            j = i + 1
            
            dx = 9999

            if j < len(enemies):
                dX = enemies[j][0] - enemies[i][0] - enemies[i][2]

                if dX <= 10:
                    if enemies[j][1] < enemies[i][1]:
                        enemies[i][1] = enemies[j][1]
                        enemies[i][3] = enemies[j][3]

                    enemies[i][2] = enemies[j][2] + enemies[i][2] + dX
            
                    enemies.remove(enemies[j])
                    i -= 1
            i += 1

        return enemies

    def __setCurrentSpeed(self, enemies):
        if len(enemies) > 0:
            if enemies[0][0] > 1000 and self.__ableToMeasure == False:
                self.__ableToMeasure = True

            elif self.__ableToMeasure == True and enemies[0][0] < 1000 and self.__stopwatch is None:
                self.__stopwatch = StopWatch()
                self.__stopwatch.start()
                            
            elif enemies[0][0] < 400 and self.__ableToMeasure == True:
                self.__ableToMeasure = False
                self.__stopwatch.stop()
                elapsedTime = self.__stopwatch.get_elapsed_time()

                if elapsedTime < self.__dt:
                    self.__dt = elapsedTime
                    print(f"current speed: {self.__dt}")

                self.__stopwatch = None

    def __drawEnemies(self, enemies, imgCrop):
        for enemy in enemies[:]:
            cv2.rectangle(
                imgCrop, 
                (enemy[0], enemy[1]), 
                (enemy[0] + enemy[2], enemy[1] + enemy[3]), 
                (0, 0, 0), 
                2)

            cv2.imshow('Contours', imgCrop)
            cv2.waitKey(1)

    def __getDistanceSensor(self, enemies):
        dx = 0
        dy = 0

        if(len(enemies) > 0 and self.__dino is not None):
            dx = enemies[0][0] - 148
            dy = self.__dino[1] - enemies[0][1]

        return dx, dy

    def resetCurrentSpeed(self):
        self.__stopwatch = None
        self.__ableToMeasure = False
        self.__dt = 999999

    def getClosestEnemy(self):
        imgArray = self.__getLastestFrame()

        if(imgArray is not None):
            contours, imgCrop =  self.__findImageContours(imgArray)
            enemies = self.__getEnemiesFromContours(contours)
            enemies = self.__groupClosestEnemies(enemies)
            self.__setCurrentSpeed(enemies)
            #self.__drawEnemies(enemies, imgCrop)
            self.__dx, self.__dy = self.__getDistanceSensor(enemies)

            return self.__dx, self.__dy, self.__dt
            
        return self.__dx, self.__dy, self.__dt

