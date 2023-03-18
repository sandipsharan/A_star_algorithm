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

def Action_1(c2c, pos, move, end):
    the = -60*np.pi/180
    
    current_position = ((pos[0] + move*np.cos(pos[2]+the)), (pos[1]+move*np.sin(pos[2]+the)), np.ceil(pos[2]*np.pi/180+the)*(180/np.pi))
    cost2_come = c2c+move
    cost2_go = np.sqrt((end[0]-current_position[0])**2 + (end[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    node = (final_cost, cost2_come, current_position)
    if current_position not in visited_nodes and current_position not in obstacle_space:
        queue_nodes.put(node)
        path_dict[current_position] = pos
    return 

def Action_2(c2c, pos, move, end):
    the = -30*np.pi/180
    current_position = ((pos[0] + move*np.cos(pos[2]+the)), (pos[1]+move*np.sin(pos[2]+the)), np.ceil(pos[2]*np.pi/180+the)*(180/np.pi))
    cost2_come = c2c+move
    cost2_go = np.sqrt((end[0]-current_position[0])**2 + (end[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    node = (final_cost, cost2_come, current_position)
    if current_position not in visited_nodes and current_position not in obstacle_space:
        queue_nodes.put(node)
        path_dict[current_position] = pos
    return 

def Action_3(c2c, pos, move, end):
    the = 0*np.pi/180
    current_position = ((pos[0] + move*np.cos(pos[2]+the)), (pos[1]+move*np.sin(pos[2]+the)), np.ceil(pos[2]*np.pi/180+the)*(180/np.pi))
    cost2_come = c2c+move
    cost2_go = np.sqrt((end[0]-current_position[0])**2 + (end[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    node = (final_cost, cost2_come, current_position)
    if current_position not in visited_nodes and current_position not in obstacle_space:
        queue_nodes.put(node)
        path_dict[current_position] = pos
    return 

def Action_4(c2c, pos, move, end):
    the = 30*np.pi/180
    current_position = ((pos[0] + move*np.cos(pos[2]+the)), (pos[1]+move*np.sin(pos[2]+the)), np.ceil(pos[2]*np.pi/180+the)*(180/np.pi))
    cost2_come = c2c+move
    cost2_go = np.sqrt((end[0]-current_position[0])**2 + (end[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    node = (final_cost, cost2_come, current_position)
    if current_position not in visited_nodes and current_position not in obstacle_space:
        queue_nodes.put(node)
        path_dict[current_position] = pos
    return 

def Action_5(c2c, pos, move, end):
    the = 60*np.pi/180
    current_position = ((pos[0] + move*np.cos(pos[2]+the)), (pos[1]+move*np.sin(pos[2]+the)), np.ceil(pos[2]*np.pi/180+the)*(180/np.pi))
    cost2_come = c2c+move
    cost2_go = np.sqrt((end[0]-current_position[0])**2 + (end[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    node = (final_cost, cost2_come, current_position)
    
    if current_position not in visited_nodes and current_position not in obstacle_space:
        queue_nodes.put(node)
        path_dict[current_position] = pos
    return 

# For back tracking to initial position
def back_tracking(path, initial_state, pre_queue):
    best_path = []
    queue_pop_tup = pre_queue[2]
    queue_pop_initial = initial_state[2]
    best_path.append(queue_pop_tup)
    parent_node = path[queue_pop_tup]
    best_path.append(parent_node)

    while parent_node != queue_pop_initial:
        parent_node = path[parent_node]
        best_path.append(parent_node)
        if pre_queue == queue_pop_initial:
            parent_node = path[queue_pop_tup]
            best_path.append(parent_node)
            break
    best_path.reverse()
    print("Path Taken: ")
    for i in best_path:
        print(i)
    return best_path

obstacle_space = map_plot()
initial_state = (6, 6, 0)
node_state_g = (30, 30, 0)
step = 1
cc = 0
euclidean_distance = np.sqrt((node_state_g[0]-initial_state[0])**2 + (node_state_g[1]-initial_state[1])**2)
total_cost = euclidean_distance + cc
node_state_i = (total_cost, cc, (initial_state))
queue_nodes = PriorityQueue()
path_dict = {}
cost_dict = {}
visited_nodes = OrderedSet()
queue_nodes.put(node_state_i)
theta_1 = -60*np.pi/180
theta_2 = -30*np.pi/180
theta_3 = 0*np.pi/180
theta_4 = 30*np.pi/180
theta_5 = 60*np.pi/180

while True:
    queue_pop = queue_nodes.get()
    visited_nodes.add(queue_pop[2])
    position = queue_pop[2]
    x, y, theta = position
    if int(x) != node_state_g[0] and int(y) != node_state_g[1]:
        if (x+ step*np.cos(theta+theta_1)) <= 600 and (y + step*np.sin(theta+theta_1)) <= 250:
            Action_1(cc, position, step, node_state_g)
        if (x+ step*np.cos(theta+theta_1)) <= 600 and (y + step*np.sin(theta+theta_1)) <= 250:
            Action_2(cc, position, step, node_state_g)
        if (x+ step*np.cos(theta+theta_1)) <= 600 and (y + step*np.sin(theta+theta_1)) <= 250:
            Action_3(cc, position, step, node_state_g)
        if (x+ step*np.cos(theta+theta_1)) <= 600 and (y + step*np.sin(theta+theta_1)) <= 250:
            Action_4(cc, position, step, node_state_g)
        if (x+ step*np.cos(theta+theta_1)) <= 600 and (y + step*np.sin(theta+theta_1)) <= 250:
            Action_5(cc, position, step, node_state_g)

    else: 
        d = back_tracking(path_dict, node_state_i, queue_pop)
        print("Success")
        break