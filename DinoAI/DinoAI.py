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
from Vision import Vision
from CollectData import CollectData

distX = 999999
distY = 999999
currentSpeed = 999999

print('----------- Menu ----------')
print('1 - Collect training data')
print('2 - Set neural training')
print('3 - Neural Play')
print('---------------------------')
choice = input()

if choice == '1':
    vision = Vision(0)
    collectData = CollectData(vision, distX, distY, currentSpeed)
    listener = collectData.keyboardListening()

    while(True and collectData.exit == False):
        collectData.distX, collectData.distY, collectData.currentSpeed = vision.getClosestEnemy()

    listener.stop()
    listener.join()