import numpy as np
import csv
from pynput import keyboard
from datetime import datetime

class CollectData:
    def __init__(self, vision):
        self.__vision = vision
        self.distX = 999999
        self.distY = 999999
        self.exit = False
        self.currentSpeed = 999999
        self.data = None

    def __keyboardEvent(self, key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k in ['up', 'down', 'e', 'r']:  # keys of interest
            # self.keys.append(k)  # store it in global-like variable

            if(k == 'r'): 
                self.__vision.resetCurrentSpeed()
                self.__saveCsv()
                self.data = None

            elif k == 'e':
                self.__saveCsv()
                self.data = None
                self.exit = True
            
            else: 
                print(f"[{k}, {self.distX}, {self.distY}, {self.currentSpeed}]")
                newrow = [k, self.distX, self.distY, self.currentSpeed]
                
                if self.data is None: self.data = newrow
                else: self.data = np.vstack([ self.data, newrow  ])

    def __saveCsv(self):
        fileName = datetime.now().strftime("%Y-%m-%d %H-%M-%S.csv")
        with open('data/' + fileName, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['cmd', 'dx', 'dy', 'speed'])

            if isinstance(self.data, list):
                writer.writerow(self.data)
            
            else:
                for dataLine in self.data:
                    writer.writerow(dataLine)

    def keyboardListening(self):
        listener = keyboard.Listener(on_press=self.__keyboardEvent)
        listener.start()  # start to listen on a separate thread
        
        return listener

