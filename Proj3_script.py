from queue import PriorityQueue
import numpy as np
import pygame
from sortedcollections import OrderedSet

# Function for finding obstacles
def map_plot():
    obstacle = OrderedSet()
    for x in range (0,601, 1):
        for y in range(0, 251, 1):
            if  (95 <= x <= 155) and (0 <= y <= 105):
                obstacle.add((x,y))
            if  (95 <= x <= 155) and (145 <= y <= 250):
                obstacle.add((x,y))
            if  (y +2*x - 1156) < 0 and (y- 2*x + 906) > 0 and (455 <= x) and (20 <= y <= 230):
                obstacle.add((x,y))
            if  (y - (15/26)*x - (425/13)) < 0 and (y + (15/26)*x - (4925/13)) < 0 and (y - (15/26)*x + (1675/13)) > 0 and (y + (15/26)*x - (2825/13)) > 0 and (230 <= x <= 370):
                obstacle.add((x,y))
            if  (100 <= x <= 150) and (0 <= y <= 100):
                obstacle.add((x,y))
            if  (100 <= x <= 150) and (150 <= y <= 250):
                obstacle.add((x,y))
            if  (y +2*x - 1145) < 0 and (y- 2*x + 895) > 0 and (460 <= x) and (20 <= y <= 230):
                obstacle.add((x,y))
            if  (y - (15/26)*x - (350/13)) < 0 and (y + (15/26)*x - (4850/13)) < 0 and (y - (15/26)*x + (1600/13)) > 0 and (y + (15/26)*x - (2900/13)) > 0 and (235 <= x <= 365):
                obstacle.add((x,y))
            if (0 <= x <= 5) or (0 <= y <= 5) or (595 <= x <= 600) or (245 <= y <=250):
                obstacle.add((x,y))
    
    return obstacle
