import pandas as pd
import numpy as np
import time
from selenium import webdriver
from StopWatch import StopWatch
from Vision import Vision
from CollectData import CollectData
from selenium import webdriver
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from pynput.keyboard import Controller, Key

print('----------- Menu ----------')
print('1 - Collect training data')
print('2 - Set neural training')
print('3 - Neural Play')
print('---------------------------')
choice = input()

if choice == '1':
    vision = Vision(0)
    collectData = CollectData(vision)
    listener = collectData.keyboardListening()

    chrome_options = webdriver.ChromeOptions();
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    browser = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    browser.get("chrome://dino")

    speed = browser.execute_script("return Runner.instance_.currentSpeed");

    i = 6

    while(True and collectData.exit == False):
        collectData.distX, collectData.distY = vision.getClosestEnemy()
        collectData.currentSpeed = browser.execute_script("return Runner.instance_.currentSpeed")
        jumping = browser.execute_script(" return Runner.instance_.tRex.jumping")

        if jumping == False:
            collectData.insertNonActionRow()

    listener.stop()
    listener.join()

if choice == '2':
    data = pd.read_csv('data/data.csv')
    
    x = data.iloc[:, 0:3]
    y = data.iloc[:, 3]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)
    
    nn = MLPClassifier(activation='logistic', solver='sgd', hidden_layer_sizes=(2000,), random_state=7, max_iter=300, learning_rate_init=0.001)
    nn.fit(x_train, y_train)

    pred = nn.predict(x_test)
    count = 0

    for i in range(len(pred)):
        if pred[i] == y_test.values[i]:
            count = count + 1

    print(count)
    print(len(pred))
    print(count / len(pred))

if choice == '3':
    keyboard = Controller()

    data = pd.read_csv('data/data.csv')
    
    x = data.iloc[:, 0:3]
    y = data.iloc[:, 3]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)
    
    nn = MLPClassifier(activation='logistic', solver='sgd', hidden_layer_sizes=(500), random_state=7, max_iter=300, learning_rate_init=0.001)
    nn.fit(x_train, y_train)

    chrome_options = webdriver.ChromeOptions();
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    browser = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    browser.get("chrome://dino")

    vision = Vision(0)

    time.sleep(10)

    keyboard.press(Key.up)
    time.sleep(0.015)
    keyboard.release(Key.up)

    while True:
        dx, dy = vision.getClosestEnemy()
        speed = browser.execute_script("return Runner.instance_.currentSpeed")
        jumping = browser.execute_script(" return Runner.instance_.tRex.jumping")

        if dy >= -25 and jumping == False:
            pred = nn.predict([[dx, dy, speed]])

            if pred == 1:
                time.sleep(0.01)
                keyboard.press(Key.up)
                keyboard.release(Key.up)
                
                print(f"{dx} {dy} {speed} {pred}")