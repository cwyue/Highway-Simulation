import random
import time
random.seed(time.time())


class Vehicle:
    def __init__(self, base=0, id=-1):
        self.vMax = random.randint(7-base, 9-base)
        self.speed = random.randint(3, 8-base)
        self.id = id
        # initialize the speed of one vehicle
        
    def changeSpeed(self, v):
        self.speed = v
