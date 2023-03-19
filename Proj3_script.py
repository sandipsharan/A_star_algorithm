import numpy as np
import time
import pygame
import vidmaker
from sortedcollections import OrderedSet
import heapdict


def round_off(number):
    return round(number * 2) / 2


def roundThirty(x):
    if x % 30 < 15:
        return x - x % 30
    else:
        return x + 30 - x % 30


def clearance(d, a):
    Hm1 = Hm3 = (-15/26)
    Hm2 = Hm4 = (15/26)
    Hc1, Hc2, Hc3, Hc4, Hc5, Hc6 = (
        4850/13), (350/13), (2900/13), -(1600/13), 235, 365
    Tm1, Tm2 = -2, 2
    Tc1, Tc2, Tc3 = 1145, -895, 460
    phc1 = parallel_line_finder(Hm1, Hc1, d, 'Greater')
    phc2 = parallel_line_finder(Hm2, Hc2, d, 'Greater')
    phc3 = parallel_line_finder(Hm3, Hc3, d, 'Lesser')
    phc4 = parallel_line_finder(Hm4, Hc4, d, 'Lesser')
    ptc1 = parallel_line_finder(Tm1, Tc1, d, 'Greater')
    ptc2 = parallel_line_finder(Tm2, Tc2, d, 'Lesser')
    if a == 1:
        return phc1, phc2, phc3, phc4, ptc1, ptc2
    hx1 = line_intersection(Hm1, Hm2, phc1, phc2, 1, 1)
    hx2 = line_intersection(Hm1, -1, phc1, Hc6+d, 1, 0)
    hx3 = line_intersection(Hm4, -1, phc4, Hc6+d, 1, 0)
    hx4 = line_intersection(Hm3, Hm4, phc3, phc4, 1, 1)
    hx5 = line_intersection(Hm3, -1, phc3, Hc5-d, 1, 0)
    hx6 = line_intersection(Hm2, -1, phc2, Hc5-d, 1, 0)
    Tx1 = line_intersection(Tm1, Tm2, ptc1, ptc2, 1, 1)
    Tx2 = line_intersection(Tm1, 0, ptc1, 225+d, 1, 1)
    Tx3 = [Tc3 - d, 225+d]
    Tx4 = [Tc3 - d, 25-d]
    Tx5 = line_intersection(Tm2, 0, ptc2, 25-d, 1, 1)
    return hx1, hx2, hx3, hx4, hx5, hx6, Tx1, Tx2, Tx3, Tx4, Tx5


def line_intersection(m1, m2, c1, c2, a, b):
    A = np.array([[-m1, a], [-m2, b]])
    B = np.array([c1, c2])
    X = np.linalg.solve(A, B)
    return X


def parallel_line_finder(m, c, d, str):
    c21 = c + d*np.sqrt(m**2 + 1)
    c22 = c - d*np.sqrt(m**2 + 1)
    if str == 'Greater':
        if c21 > c:
            return c21
        else:
            return c22
    else:
        if c21 < c:
            return c21
        else:
            return c22


def coords_pygame(coords, height):
    return (coords[0], height - coords[1])


def rect_pygame(coords, height, obj_height):
    return (coords[0], height - coords[1] - obj_height)


def create_map(d, hx1, hx2, hx3, hx4, hx5, hx6, Tx1, Tx2, Tx3, Tx4, Tx5):
    pygame.init()
    size = [600, 250]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Visualization")
    screen.fill("white")
    x, y = rect_pygame([100-d, 0], 250, 100+d)
    pygame.draw.rect(screen, "blue", [x, y, 50+2*d, 100+d], 0)
    x, y = rect_pygame([100, 0], 250, 100)
    pygame.draw.rect(screen, "red", [x, y, 50, 100], 0)
    x, y = rect_pygame([100-d, 150-d], 250, 100+d)
    pygame.draw.rect(screen, "blue", [x, y, 50+2*d, 100+d], 0)
    a, b = rect_pygame([100, 150], 250, 100)
    pygame.draw.rect(screen, "red", [a, b, 50, 100], 0)
    pygame.draw.rect(screen, "blue", [0, 0, d, 250], 0)
    pygame.draw.rect(screen, "blue", [0, 0, 600, d], 0)
    pygame.draw.rect(screen, "blue", [0, 250-d, 600, d], 0)
    pygame.draw.rect(screen, "blue", [600-d, 0, d, 250], 0)
    a, b = coords_pygame(Tx1, 250)
    c, d = coords_pygame(Tx2, 250)
    e, f = coords_pygame(Tx3, 250)
    g, h = coords_pygame(Tx4, 250)
    i, j = coords_pygame(Tx5, 250)
    pygame.draw.polygon(
        screen, "blue", ([a, b], [c, d], [e, f], [g, h], [i, j]), 0)
    a, b = coords_pygame([460, 25], 250)
    c, d = coords_pygame([460, 225], 250)
    e, f = coords_pygame([510, 125], 250)
    pygame.draw.polygon(screen, "red", [[a, b], [c, d], [e, f]], 0)
    a, b = coords_pygame(hx1, 250)
    c, d = coords_pygame(hx2, 250)
    e, f = coords_pygame(hx3, 250)
    g, h = coords_pygame(hx4, 250)
    i, j = coords_pygame(hx5, 250)
    k, l = coords_pygame(hx6, 250)
    pygame.draw.polygon(screen, "blue", [[a, b], [c, d], [
                        e, f], [g, h], [i, j], [k, l]], 0)
    pygame.draw.polygon(screen, "red", ((235, 87.5), (300, 50),
                        (365, 87.5), (365, 162.5), (300, 200), (235, 162.5)))
    # pygame.display.flip()
    # pygame.time.wait(3000)
    pygame.quit()


def check_obstacles(d, phc1, phc2, phc3, phc4, ptc1, ptc2):
    obstacles = OrderedSet()
    for x in range(0, 601):
        for y in range(0, 251):
            if (x >= (235 - d) and x <= (365+d) and (y-((15/26)*x) - phc2) <= 0
                and (y+((15/26)*x) - phc1) <= 0 and (y+((15/26)*x) - phc3) >= 0
                    and (y-((15/26)*x) + phc4) >= 0):
                obstacles.add((x, y))
            if (x >= (100-d) and y >= 0 and x <= (150+d) and y <= (100+d)):
                obstacles.add((x, y))
            if (x >= (100-d) and y >= (150-d) and x <= (150+d) and y <= 250):
                obstacles.add((x, y))
            if (x >= (600-d) or y >= (250-d) or x <= d or y <= d):
                obstacles.add((x, y))
            if (x >= (460-d) and (y+(2*x) - ptc1) <= 0 and y <= (225+d) and y >= (25-d) and (y-2*x + ptc2) >= 0):
                obstacles.add((x, y))
    return obstacles


def input_start(str):
    while True:
        print("Enter", str, "(Sample: 10, 10, 30): ")
        A = [int(i) for i in input().split(', ')]
        A_1 = (A[0], A[1], A[2])
        if str == 'Step, Clearance and Radius':
            if 1 <= A_1[0] <= 10:
                return A_1
            else:
                print(
                    "The entered step size should be in the range of 1 to 10, please try again")
        else:
            if (A[0], A[1]) in obstacle_space:
                print(
                    "The entered input lies on the obstacles (or) not valid, please try again")
            else:
                return A_1


def Action_1(c2c, pos):
    current_position = (round_off(pos[0] + step*np.cos(np.deg2rad(pos[2])+theta_1)), round_off(pos[1] + step*np.sin(np.deg2rad(pos[2])+theta_1)),
                        roundThirty((np.deg2rad(pos[2])+theta_1)*(180/np.pi)))
    cost2_come = c2c+step
    if current_position[2] > 180 or current_position[2] < -180:
        current_position = (current_position[0], current_position[1], 0)
    cost2_go = np.sqrt((node_state_g[0]-current_position[0])**2 +
                       (node_state_g[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    if Accum[int(current_position[0]*2), int(current_position[1]*2), int(current_position[2]/30)] != 1 and current_position not in obstacle_space:
        queue_nodes[current_position] = final_cost, cost2_come
        path_dict[(current_position[0], current_position[1])] = (
            pos[0], pos[1])
    return


def Action_2(c2c, pos):
    current_position = (round_off(pos[0] + step*np.cos(np.deg2rad(pos[2])+theta_2)), round_off(pos[1] + step*np.sin(np.deg2rad(pos[2])+theta_2)),
                        roundThirty((np.deg2rad(pos[2])+theta_2)*(180/np.pi)))
    cost2_come = c2c+step
    if current_position[2] > 180 or current_position[2] < -180:
        current_position = (current_position[0], current_position[1], 0)
    cost2_go = np.sqrt((node_state_g[0]-current_position[0])**2 +
                       (node_state_g[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    if Accum[int(current_position[0]*2), int(current_position[1]*2), int(current_position[2]/30)] != 1 and current_position not in obstacle_space:
        queue_nodes[current_position] = final_cost, cost2_come
        path_dict[(current_position[0], current_position[1])] = (
            pos[0], pos[1])
    return


def Action_3(c2c, pos):
    current_position = (round_off(pos[0] + step*np.cos(np.deg2rad(pos[2])+theta_3)), round_off(pos[1] + step*np.sin(np.deg2rad(pos[2])+theta_3)),
                        roundThirty((np.deg2rad(pos[2])+theta_3)*(180/np.pi)))
    cost2_come = c2c+step
    if current_position[2] > 180 or current_position[2] < -180:
        current_position = (current_position[0], current_position[1], 0)
    cost2_go = np.sqrt((node_state_g[0]-current_position[0])**2 +
                       (node_state_g[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    if Accum[int(current_position[0]*2), int(current_position[1]*2), int(current_position[2]/30)] != 1 and current_position not in obstacle_space:
        queue_nodes[current_position] = final_cost, cost2_come
        path_dict[(current_position[0], current_position[1])] = (
            pos[0], pos[1])
    return


def Action_4(c2c, pos):
    current_position = (round_off(pos[0] + step*np.cos(np.deg2rad(pos[2])+theta_4)), round_off(pos[1] + step*np.sin(np.deg2rad(pos[2])+theta_4)),
                        roundThirty((np.deg2rad(pos[2])+theta_4)*(180/np.pi)))
    cost2_come = c2c+step
    if current_position[2] > 180 or current_position[2] < -180:
        current_position = (current_position[0], current_position[1], 0)
    cost2_go = np.sqrt((node_state_g[0]-current_position[0])**2 +
                       (node_state_g[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    if Accum[int(current_position[0]*2), int(current_position[1]*2), int(current_position[2]/30)] != 1 and current_position not in obstacle_space:
        queue_nodes[current_position] = final_cost, cost2_come
        path_dict[(current_position[0], current_position[1])] = (
            pos[0], pos[1])
    return


def Action_5(c2c, pos):
    current_position = (round_off(pos[0] + step*np.cos(pos[2]+theta_5)), round_off(pos[1] + step*np.sin(pos[2]+theta_5)),
                        roundThirty((np.deg2rad(pos[2])+theta_5)*(180/np.pi)))
    cost2_come = c2c+step
    if current_position[2] > 180 or current_position[2] < -180:
        current_position = (current_position[0], current_position[1], 0)
    cost2_go = np.sqrt((node_state_g[0]-current_position[0])**2 +
                       (node_state_g[1]-current_position[1])**2)
    final_cost = cost2_come + cost2_go
    if Accum[int(current_position[0]*2), int(current_position[1]*2), int(current_position[2]/30)] != 1 and current_position not in obstacle_space:
        queue_nodes[current_position] = final_cost, cost2_come
        path_dict[(current_position[0], current_position[1])] = (
            pos[0], pos[1])
    return


def back_tracking(path, pre_queue):
    best_path = OrderedSet()
    best_path.add((pre_queue[0][0], pre_queue[0][1]))
    parent_node = path[(pre_queue[0][0], pre_queue[0][1])]
    best_path.add(parent_node)
    while parent_node != (initial_state[0], initial_state[1]):
        parent_node = path[parent_node]
        best_path.add(parent_node)
        if (pre_queue[0][0], pre_queue[0][1]) == (initial_state[0], initial_state[1]):
            parent_node = path[(pre_queue[0][0], pre_queue[0][1])]
            best_path.add(parent_node)
            break
    final_path = sorted(best_path, reverse=False)
    print("Path Taken: ")
    for i in final_path:
        print(i)
    return final_path


d = 5
r = 5
# step, d, r = input_start('Step, Clearance and Radius')
phc1, phc2, phc3, phc4, ptc1, ptc2 = clearance(d+r, 1)
obstacle_space = check_obstacles((d+r), phc1, phc2, phc3, phc4, ptc1, ptc2)
hx1, hx2, hx3, hx4, hx5, hx6, Tx1, Tx2, Tx3, Tx4, Tx5 = clearance(d, 0)
create_map(d, hx1, hx2, hx3, hx4, hx5, hx6, Tx1, Tx2, Tx3, Tx4, Tx5)
# initial_state = input_start('Start Node')
# node_state_g = input_start('Goal Node')
Accum = np.zeros((1200, 500, 12))


initial_state = (11, 11, 0)
node_state_g = (30, 30, 0)
step = 1
cc = 0
euclidean_distance = np.sqrt(
    (node_state_g[0]-initial_state[0])**2 + (node_state_g[1]-initial_state[1])**2)
total_cost = euclidean_distance + cc
queue_nodes = heapdict.heapdict()
path_dict = {}
visited_nodes = OrderedSet()
queue_nodes[(initial_state)] = total_cost, cc
theta_1 = -60*np.pi/180
theta_2 = -30*np.pi/180
theta_3 = 0*np.pi/180
theta_4 = 30*np.pi/180
theta_5 = 60*np.pi/180

while (len(queue_nodes) != 0):
    queue_pop = queue_nodes.popitem()
    visited_nodes.add(queue_pop[0])
    position = queue_pop[0]
    x, y, theta = position
    cc = queue_pop[1][1]
    if Accum[int(x*2)][int(2*y)][int(theta/30)] != 1:
        Accum[int(x*2)][int(2*y)][int(theta/30)]  = 1
        if int(x) != node_state_g[0] and int(y) != node_state_g[1]:
            if (x + step*np.cos(np.deg2rad(theta)+theta_1)) <= 600 and (y + step*np.sin(np.deg2rad(theta)+theta_1)) <= 250:
                Action_1(cc, position)
            if (x + step*np.cos(np.deg2rad(theta)+theta_1)) <= 600 and (y + step*np.sin(np.deg2rad(theta)+theta_1)) <= 250:
                Action_2(cc, position)
            if (x + step*np.cos(np.deg2rad(theta)+theta_1)) <= 600 and (y + step*np.sin(np.deg2rad(theta)+theta_1)) <= 250:
                Action_3(cc, position)
            if (x + step*np.cos(np.deg2rad(theta)+theta_1)) <= 600 and (y + step*np.sin(np.deg2rad(theta)+theta_1)) <= 250:
                Action_4(cc, position)
            if (x + step*np.cos(np.deg2rad(theta)+theta_1)) <= 600 and (y + step*np.sin(np.deg2rad(theta)+theta_1)) <= 250:
                Action_5(cc, position)
        else:
            back_track = back_tracking(path_dict, queue_pop)
            print("Goal reached")
            break
