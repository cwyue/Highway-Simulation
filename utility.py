import matplotlib.pyplot as plt
import math
import settings

colors = ['r', 'b', 'm', 'g', 'y', 'k', 'c', 'r']

def dist_2pt(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def base_map_plotter(basemap):
    plt.figure (1, figsize=(8, 8))
    axes = plt.gca ()
    axes.set_xlim ([-500, 3750])
    axes.set_ylim ([-500, 3750])
    plt.grid (True)
    i=0
    for rd in basemap:
        plt.scatter (*zip(*rd), s=2, color=colors[i])
        i+=1
    
    # plt.scatter ([10, 50], [10, 50], s=5, c='r', marker=(5, 2))  # for checking scales
    plt.show ()
 
    
def realtime_plotter(lanes):
    plt.figure (2, figsize=(8, 8))
    axes = plt.gca ()
    axes.set_xlim ([-500, 3750])
    axes.set_ylim ([-500, 3750])
    plt.grid (True)
    X = []
    Y = []
    for lane in lanes:
        for c in lane.cells:
            if c.veh is not None:
                X.append(c.x)
                Y.append(c.y)
    plt.scatter(X, Y, s=1)
    plt.show()

def color_plotter(x, y):
    plt.figure (1, figsize=(8, 8))
    axes = plt.gca ()
    axes.set_xlim ([-500, 3750])
    axes.set_ylim ([-500, 3750])
    plt.grid (True)

    for i in range(len(x)):
        plt.scatter (x[i], y[i], s=0.5, color=colors[i])
    plt.show()