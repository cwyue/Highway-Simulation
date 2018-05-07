import settings
import lane
import random
import vehicle

class MergeLane:
    # 40 ft/s for in-merging lanes: 4 cells/s
    def __init__(self, vMax1, vMax2):
        vm = [vMax1, vMax2]
        ln = [settings.L1, settings.L2]
        self.lanes = [lane.Lane(ln[i], vm[i], 0.1, i+5) for i in range(2)]
        self.cell_size = settings.CELL_SIZE
        self.e_prob1 = 0.5
        self.e_prob2 = 0.5
    
    def update_speed(self):
        for lane in self.lanes:
            lane.update_speed(4, 70, 50, 1, end=True)

    def update_position(self):
        for lane in self.lanes:
            lane.update_position(end=True, end_pts=3)

    def enter_at_start(self, prob1, prob2):
        for i in range(3):
            if random.random() < prob1:
                self.lanes[0].addCar(vehicle.Vehicle(base=4, id=5), 4*i)
        for i in range(4):
            if random.random() < prob2:
                self.lanes[1].addCar(vehicle.Vehicle(base=4, id=6), 4*i)

    def update_states(self):
        self.enter_at_start (self.e_prob1, self.e_prob2)
        self.update_speed ()
        self.update_position ()