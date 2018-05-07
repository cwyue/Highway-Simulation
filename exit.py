import settings
import lane
import random
import vehicle


class ExitLane:
    # 40 ft/s for exit lanes: 4 cells/s
    def __init__(self, vMax):
        ln = settings.L3
        self.lanes = lane.Lane (ln, vMax, 0.1, 7)
        self.cell_size = settings.CELL_SIZE
    
    def update_speed(self):
        self.lanes.update_speed (3, 70, 50, 1, end=True)
    
    def update_position(self):
        self.lanes.update_position (end=True, end_pts=3)
    
    def exit_at_end(self):
       for i in range(len(self.lanes.cells) - 5, len(self.lanes.cells)):
            if self.lanes.cells[i] is not None:
                    self.lanes.RemoveCar(i)
    
    def update_states(self):
        self.exit_at_end()
        self.update_speed()
        self.update_position()
