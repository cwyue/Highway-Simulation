import vehicle
import random
import settings
import time

# one single lane
class Lane:
    def __init__(self, l, vMax, density, id):
        random.seed(time.time())
        # density = total number of vehicles / total number of cells
        self.density = density  # initialize the vehicle density of one highway
        self.vMax = vMax  # max speed for all vehicles in this lane
        self.size = l  # initialize the number of cells of one highway (unit length: 10 meters) #### updated: 5m
        self.cells = [None] * self.size  # initialize the cell array
        self.cell_size = settings.CELL_SIZE
        base = 0
        if id > 4:
            base = 4
        # initialize some vehicles in the lane
        randvar = int(l/100)
        num = min(int(density * l) + random.randint(-randvar, randvar), l-22)   # adding some variance in the distribution
        pos = random.sample(xrange(6, l-6), num)
        
        for p in pos:
            self.cells[p] = vehicle.Vehicle(base=base, id=id)
        
        self.vNum = num  # number of vehicles in this lane
        self.hasAccident = False  # one lane has no car accidents at the beginning
    
    # add a new vehicle into a given position of one lane
    def addCar(self, car, position):
        if (self.cells[position] == None):
            self.cells[position] = car
            self.vNum = self.vNum + 1
            return True
        else:
            return False
    
    def RemoveCar(self, position):
        if (self.cells[position] != None):
            car = self.cells[position]
            self.vNum = self.vNum - 1
            self.cells[position] = None;
            return car

    def update_speed(self, end_pts, speed_up_dist, slow_down_dist, vlow, end=False, accident=None):
        vnew = [-1] * self.size
        if accident != None and len(self.cells) > 250:
            for m in range(248, 251):
                if self.cells[m] != None:
                    self.cells[m].speed = 0
                    
        if end == True:
            for i in range(1, 4):
                if self.cells[i] != None:
                    self.cells[i].speed = 0
        for i in range (3, self.size - end_pts):
            if self.cells[i] != None:
                assert self.cells[i].speed >= 0
                # stop if any vehicle appears right in front of you or one cell (10 feet) away
                if self.cells[i + 1] != None or self.cells[i + 2] != None:
                    vnew[i] = 0
                else:
                    # current vehicle starts to move if the speed of the current vehicle is 0
                    # and the vehicle ahead has already been more than 30 feet away [i+1 ~ i+3]
                    if self.cells[i].speed == 0 and all (
                            c == None for c in self.cells[min (i + 1, self.size - 1): min (i + 4, self.size - 1)]):
                        vnew[i] = 2
                    if self.cells[i].speed == 0 and all (
                            c == None for c in self.cells[min (i + 1, self.size - 1): min (i + 6, self.size - 1)]):
                        vnew[i] = min(4, self.vMax-1)
                    # speed up if no vehicle within the range of "speed_up_dist" ft ahead of you
                    elif (int (speed_up_dist / self.cell_size + 1) < self.size - 1) and all (
                            c == None for c in self.cells[i + 1: i + int (speed_up_dist / self.cell_size + 1)]):
                        vnew[i] = min (self.cells[i].speed + 2, self.vMax + 1)
                    # slow down if any vehicle ahead is slower than you in the range of "slow_down_dist" ft ahead of you
                    # make sure the speed cannot go down to 0 (reduce to vlow)
#                    else:
#                        flag = False
#                        for j in range (1, int (slow_down_dist / self.cell_size + 1)):
#                            if i + j > self.size - 1:
#                                break
#                            if self.cells[i + j] != None and self.cells[i].speed > self.cells[i + j].speed:
#                                flag = True
#                                id = i + j
#                                break
#                        if flag:
#                            vnew[i] = max (self.cells[id].speed, vlow)
        
        # update the speed of all vehicles after checking of the complete self has been finished
        for i in range (len (vnew)):
            if vnew[i] >= 0:
                self.cells[i].speed = vnew[i]

    def update_position(self, start=False, start_pts=0, end=False, end_pts=0, accident= None):
        for i in range(self.size - 1, -1, -1):
            if self.cells[i] != None:
                if self.cells[i].speed == 0:
                    continue
                newPos = i + self.cells[i].speed  # calculate which cell this vehicle will move to
                if i < 250 and newPos >= 250:
                    if accident != None:
                        self.cells[i].speed = 0
                        flag = False
                        for k in range (i + 1, 251):
                            if self.cells[k] != None:
                                flag = True
                                break
                        if flag:
                            self.cells[k - 1] = self.cells[i]
                            self.cells[i] = None
                        else:
                            self.cells[250] = self.cells[i]
                            self.cells[i] = None
                elif newPos >= self.size - 1 - end_pts and end == True:
                    self.cells[i].speed = 0
                    flag = False
                    for k in range (i + 1, self.size):
                        if self.cells[k] != None:
                            flag = True
                            break
                    if flag:
                        self.cells[k - 1] = self.cells[i]
                        self.cells[i] = None
                    else:
                        self.cells[-1] = self.cells[i]
                        self.cells[i] = None
                elif newPos > self.size - 1:
                    self.cells[i] = None
                elif all (c == None for c in self.cells[i + 1: newPos + 1]):
                    self.cells[newPos] = self.cells[i]
                    self.cells[i] = None
                else:
                    for j in range (i + 1, newPos + 1):
                        if self.cells[j] != None:
                            self.cells[j] = self.cells[i]
                            self.cells[j].speed = 0
                            self.cells[i] = None
                            break

    def update_speed_basecase(self, end_pts, speed_up_dist, slow_down_dist, vlow, end=False):
        vnew = [-1] * self.size
        if end == True:
            for i in range(1, 4):
                if self.cells[i] != None:
                    self.cells[i].speed = 0
        for i in range (3, self.size - end_pts):
            if self.cells[i] != None:
                assert self.cells[i].speed >= 0
                # stop if any vehicle appears right in front of you or one cell (10 feet) away
                if self.cells[i + 1] != None or self.cells[i + 2] != None:
                    vnew[i] = 0
                else:
                    # current vehicle starts to move if the speed of the current vehicle is 0
                    # and the vehicle ahead has already been more than 30 feet away [i+1 ~ i+3]
                    if self.cells[i].speed == 0 and all (
                            c == None for c in self.cells[min (i + 1, self.size - 1): min (i + 4, self.size - 1)]):
                        vnew[i] = 2
                    # speed up if no vehicle within the range of "speed_up_dist" ft ahead of you
                    elif (int (speed_up_dist / self.cell_size + 1) < self.size - 1) and all (
                            c == None for c in self.cells[i + 1: i + int (speed_up_dist / self.cell_size + 1)]):
                        vnew[i] = min (self.cells[i].speed + 2, self.vMax + 2)
                    # slow down if any vehicle ahead is slower than you in the range of "slow_down_dist" ft ahead of you
                    # make sure the speed cannot go down to 0 (reduce to vlow)
                    else:
                        flag = False
                        for j in range (1, int (slow_down_dist / self.cell_size + 1)):
                            if i + j > self.size - 1:
                                break
                            if self.cells[i + j] != None and self.cells[i].speed > self.cells[i + j].speed:
                                flag = True
                                id = i + j
                                break
                        if flag:
                            vnew[i] = max (self.cells[id].speed, vlow)
        
        # update the speed of all vehicles after checking of the complete self has been finished
        for i in range (len (vnew)):
            if vnew[i] >= 0:
                self.cells[i].speed = vnew[i]

    def update_position_basecase(self, start=False, start_pts=0, end=False, end_pts=0):
        for i in range(self.size - 1, -1, -1):
            if self.cells[i] != None:
                if self.cells[i].speed == 0:
                    continue
                newPos = i + self.cells[i].speed  # calculate which cell this vehicle will move to
                if newPos >= self.size - 1 - end_pts and end == True:
                    self.cells[i].speed = 0
                    flag = False
                    for k in range(i+1, self.size):
                        if self.cells[k]!= None:
                            flag = True
                            break
                    if flag:
                        self.cells[k-1] = self.cells[i]
                        self.cells[i] = None
                    else:
                        self.cells[-1] = self.cells[i]
                        self.cells[i] = None
                elif newPos > self.size - 1:
                    self.cells[i] = None
                elif all (c == None for c in self.cells[i + 1: newPos + 1]):
                    self.cells[newPos] = self.cells[i]
                    self.cells[i] = None
                else:
                    for j in range(i + 1, newPos + 1):
                        if self.cells[j] != None:
                            self.cells[j] = self.cells[i]
                            self.cells[j].speed = 0
                            self.cells[i] = None
                            break


    # get some system status of this lane (e.g., density, occurence of accidents)
    def get_parameters(self):
        self.density = self.vNum / self.size
        return self.vNum, self.density, self.hasAccident