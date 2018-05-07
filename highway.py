import multilane
import merge
import exit
import random
import settings


class Highway:
    def __init__(self):
        self.multiway = multilane.MultiLane (5, 8)
        self.mergelane = merge.MergeLane(40, 40)
        self.exitway = exit.ExitLane(40)
        
    # integrate all procedures in a single run for the main (multi-lane) highway
    def update_states(self, itern, prob, flag):
        self.merge_join()
        self.exit_leave(0.9)
        self.multiway.update_states(itern, prob, flag)
        self.mergelane.update_states()
        self.exitway.update_states()
        
    # merge 2 lanes into the 5th lane of the main highway
    # check merge lane first to find if there is any vehicle waiting
    # to merge into the main road, then check open positions on main road
    def merge_join(self):
        joins = settings.JOIN_ID[:2] # get the joint cell id
        for k in range(2):
            dt = 0
            for i in range (1, 4):  # any vehicle in the first 3 cells is considered ready for merging
                car = self.mergelane.lanes[k].cells[-i]
                if car != None:
                    pos = i
                    break
            if car != None:
                for pt in range(joins[k], joins[k]+80):
                    # cells available for merging is defined as an open cell with 80 ft open space behind
                    # and 40ft open space ahead
                    if all(c == None for c in self.multiway.lanes[k].cells[pt-8: pt+5]):
                        self.mergelane.lanes[k].cells[-pos] = None
                        if random.random()<0.5:
                            car.speed = 5
                        else:
                            car.speed = 6
                        self.multiway.lanes[4].cells[pt] = car
                        break
    
    def exit_leave(self, prob):
        join = settings.JOIN_ID[2]
        cnt = 2
        for i in range(-2, 6):
            car = self.multiway.lanes[4].cells[i+join]
            if car != None:
                if random.random()<prob:
                    flag = False
                    for j in range(5):
                        if self.exitway.lanes.cells[j] == None:
                            flag = True
                            randx = random.random ()
                            if randx < 0.1:
                                car.speed = 3
                            elif randx < 0.8:
                                car.speed = 4
                            else:
                                car.speed = 5
                            self.exitway.lanes.cells[j] = car
                            self.multiway.lanes[4].cells[i + join] = None
                            cnt -= 1
                            if cnt <= 0:
                                return
                