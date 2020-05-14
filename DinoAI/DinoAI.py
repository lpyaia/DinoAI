from selenium import webdriver
from StopWatch import StopWatch
from Vision import Vision
from CollectData import CollectData
from selenium import webdriver

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
    chrome_options.add_experimental_option("useAutomationExtension", False);
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    browser = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    browser.get("chrome://dino")

    speed = browser.execute_script("return Runner.instance_.currentSpeed");

    i = 6

    while(True and collectData.exit == False):
        collectData.distX, collectData.distY = vision.getClosestEnemy()
        collectData.currentSpeed = browser.execute_script("return Runner.instance_.currentSpeed");

    listener.stop()
    listener.join()