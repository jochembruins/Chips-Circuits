# python script
###########################################################
# functions.py
#
# Jochem Bruins
# 10578811
#
# Melle Gelok
# 11013893
#
# Noah van Grinsven
# 10501916
#
# Chips & Circuits
#
# Contains all functions used in chips.py
###########################################################
from typing import List

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from classes import *
from random import randint
from copy import deepcopy

np.set_printoptions(threshold=np.nan)
np.set_printoptions(linewidth=180)


def makeLocations(data):
    gates = []
    for line in data:
        line = Location(line[0], int(line[1]), int(line[2]), int(line[3]))
        gates.append(line)
    return gates


def makeObjects(netlist, gates):
    emptyRouteBook = []

    for point in netlist:
        locFrom = [gates[point[0]].z, gates[point[0]].y, gates[point[0]].x]
        locTo = [gates[point[1]].z, gates[point[1]].y, gates[point[1]].x]
        # surrounding gridpoints of start/end point
        fromSurround = [[gates[point[0]].z, gates[point[0]].y + 1, gates[point[0]].x],
                      [gates[point[0]].z, gates[point[0]].y - 1, gates[point[0]].x],
                      [gates[point[0]].z, gates[point[0]].y, gates[point[0]].x + 1],
                      [gates[point[0]].z, gates[point[0]].y, gates[point[0]].x - 1],
                      [gates[point[0]].z + 1, gates[point[0]].y, gates[point[0]].x]]
        toSurround = [[gates[point[1]].z, gates[point[1]].y + 1, gates[point[1]].x],
                      [gates[point[1]].z, gates[point[1]].y - 1, gates[point[1]].x],
                      [gates[point[1]].z, gates[point[1]].y, gates[point[1]].x + 1],
                      [gates[point[1]].z, gates[point[1]].y, gates[point[1]].x - 1],
                      [gates[point[1]].z + 1, gates[point[1]].y, gates[point[1]].x]]
        route = []
        emptyRoute = wire(point, locFrom, locTo, fromSurround, toSurround, route)
        # print(emptyRoute)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def printPlot(gates):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Define ticks
    ticks = np.arange(0, 18, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    for obj in gates:
        plt.plot(obj.x, obj.y, 'ro')  # WAAR KOMEN FIG EN PLOT SAMEN?
        plt.annotate(int(obj.gate), xy=(obj.x, obj.y))

    # And a corresponding grid
    plt.grid(which='both')
    plt.axis([0, 17, 12, 0])
    plt.show()
    return


def gridMat(gates):
    # make matrix of grid
    matgrid = np.zeros([12, 13, 18]) + 99

    for gate in gates:
        matgrid[gate.z, gate.y, gate.x] = gate.gate
    return matgrid


def routeFinder(routeBook, grid):
    print('in routefinder')
    routeBookEmpty = routeBook
    routeBookDone = []
    while routeBookEmpty != []:
        for netPoint in routeBookEmpty:
            route = []
            cursor = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
            locTo = [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]

            # add begin point to route
            route.append([cursor[0], cursor[1], cursor[2]])

            # select which gridpoint next to end location is free
            for nextLocTo in netPoint.toSurround:
                if grid[nextLocTo[0], nextLocTo[1], nextLocTo[2]] == 99:
                    locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]
                    break

            # if end location cant be reached, delete one of lines on surrounding gridpoints
            if [locTo[0], locTo[1], locTo[2]] == [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]:
                # check every surrounding gridpoint, delete most appropriate line
                for nextLocTo in netPoint.toSurround:
                    for netPointToDelete in routeBookDone:
                        for routepoint in netPointToDelete.route:
                            if nextLocTo == [routepoint[0], routepoint[1], routepoint[2]]:
                                if netPointToDelete.locTo != [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]] and \
                                        netPointToDelete.locFrom != [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]] and \
                                        nextLocTo != netPointToDelete.locTo:

                                    # remove line on grid
                                    grid = delRoute(netPointToDelete.route[1:-1], grid)
                                    netPointToDelete.route = []

                                    # append deleted line back to the routebookempty list

                                    routeBookEmpty.append(netPointToDelete)
                                    # delete line from routebookdone list
                                    del routeBookDone[routeBookDone.index(netPointToDelete)]
                                    locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]

                                    break
                        else:
                            continue
                        break
                    else:
                        continue
                    break

            # make first step in available direction
            for nextLocFrom in netPoint.fromSurround:
                if grid[nextLocFrom[0], nextLocFrom[1], nextLocFrom[2]] == 99:
                    cursor = [nextLocFrom[0], nextLocFrom[1], nextLocFrom[2]]
                    route.append([cursor[0], cursor[1], cursor[2]])
                    break

            # look for best step until 1 step away from endpoint
            while abs(locTo[0] - cursor[0]) + abs(locTo[1] - cursor[1]) + abs(locTo[2] - cursor[2]) > 1:

                # check if steps in y direction is bigger than x direction
                if abs(locTo[1] - cursor[1]) > abs(locTo[2] - cursor[2]):
                    # step along y axis
                    if locTo[1] > cursor[1]:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1
                else:
                    # step along x axis
                    if locTo[2] > cursor[2]:
                        cursor[2] += 1
                    else:
                        cursor[2] -= 1
                # save step in route
                route.append([cursor[0], cursor[1], cursor[2]])

                # check if previous step is possible else delete and go up z-axis
                if grid[cursor[0], cursor[1], cursor[2]] != 99:
                    del route[-1]
                    cursor = [route[-1][0], route[-1][1], route[-1][2]]
                    cursor[0] += 1
                    route.append([cursor[0], cursor[1], cursor[2]])

                    # check if route has already been there when cursor up in previous step
                    if len(route) > 3 and route[-1] == route[-3]:
                        del route[-2:]

                # if step down is possible, go down
                elif grid[cursor[0] - 1, cursor[1], cursor[2]] == 99.0 and cursor[0] > 0:
                    while grid[cursor[0] - 1, cursor[1], cursor[2]] == 99.0 and cursor[0] > 0:
                        cursor[0] -= 1
                        route.append([cursor[0], cursor[1], cursor[2]])

                # if above endpoint, go down and delete all blocking lines
                if [cursor[1], cursor[2]] == [locTo[1], locTo[2]]:
                    for netPointToDelete in routeBookDone:
                        for routepoint in netPointToDelete.route:
                            if [cursor[0] - 1, cursor[1], cursor[2]] == [routepoint[0], routepoint[1], routepoint[2]]:
                                # remove line on grid
                                grid = delRoute(netPointToDelete.route[1:-1], grid)
                                netPointToDelete.route = []

                                # append deleted like back to the routebookempty list
                                routeBookEmpty.append(netPointToDelete)
                                del routeBookDone[routeBookDone.index(netPointToDelete)]
                                cursor[0] -= 1
                                route.append([cursor[0], cursor[1], cursor[2]])
                                break

            # add end point to route
            route.append(locTo)
            route.append(netPoint.locTo)

            # print(netPoint, "locto=", locTo)
            # print(route)

            # save route in netPoint object
            netPoint.route = route

            # delete netPoint from to do list, append to done list
            doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
            routeBookDone.append(doneWire)

            # update matrix for route
            changeMat(netPoint.route[1:-1], grid)
    return routeBookEmpty, routeBookDone, grid

def changeMat(route, grid):
    for step in route:
        grid[step[0], step[1], step[2]] = 50
    return grid

def delRoute(route, grid):
    for step in route:
        grid[step[0], step[1], step[2]] = 99

    return grid


def plotLines(gates, routeBook):
    # maak een nieuwe plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # definieer assen
    ax.set_xlim([0, 18])
    ax.set_ylim([0, 13])
    ax.set_zlim([0, 9])

    # zet ticks op de assem
    ax.set_xticks(np.arange(0, 18, 1))
    ax.set_yticks(np.arange(0, 13, 1))
    ax.set_zticks(np.arange(0, 9, 1))

    # voeg labels toe
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')

    # voeg alle gates met labels toe
    for gate in gates:
        ax.scatter(gate.x, gate.y, 0)
        ax.text(gate.x, gate.y, 0, '%s' % (int(gate.gate)), size=10, zorder=1, color='k')

        # leg wires in plot zoals in het routebook
    for netPoint in routeBook:
        ax.plot([step[2] for step in netPoint.route], [step[1] for step in netPoint.route], [step[0] for step in netPoint.route])

    plt.show()

def getScore(routeBook):
    score = 0
    for route in routeBook:
        score += (len(route.route) - 1)
    return score


def hillClimb(routeBook, score, gates, steps=1000):
    bestRouteBook = deepcopy(routeBook)
    for i in range(0, 1000):
        for route in bestRouteBook:
            route.route = []
            print(route.netPoint)

        grid = gridMat(gates)
        
        newRouteBook = wire.changeRouteBook(bestRouteBook)
        
        tmp_newRouteBook = deepcopy(newRouteBook)
        
        print('lengte new routebook:  %i' % len(tmp_newRouteBook))   
        
        newRouteFound = []
        newScore = score
        finished = False
      
        try:
            newRouteFound = routeFinder(tmp_newRouteBook, grid)[1]
            finished = True
        except:
            print('not possible')
            
            
        if finished: 
            print('lengte new routebook 1:  %i' % len(tmp_newRouteBook))
            
            newScore = getScore(newRouteFound)
            print(newScore)
        
            if newScore < score:
                bestRouteBook = tmp_newRouteBook
                score = newScore
            else:
                print('hoger')


    return routeBook, score




# hier begint het Astar algoritme met bijbehorende functies
# 

# Astar(,grid)
# Astar returned uiteindelijk de wire/route van A*
# def Astar(gates, wire, grid):
#     locfrom = [gates[wire[0]].x, gates[wire[0]].y, gates[wire[0]].z]
#     gridwithnodes = grid
#     locto = [gates[wire[0]].x, gates[wire[1]].y, gates[wire[1]].z]
#
#     route = putwire(gridwithnodes, locfrom, locto)
#     return route
#
# # putwire plaatst nodes totdat de locatie bereikt is
# def putwire(gridwithnodes, locfrom, locto):
#     start = locfrom
#     while (distance(start, locto) != 1):
#         gridwithnodes = putnodes(start, gridwithnodes, locto, locfrom)
#         start = minimumnodes(gridwithnodes)
#     route = findroute(gridwithnodes, locfrom, locto)
#     return route
#
# #  nodes plaatsen
# def putnodes(start, grid, destination, locfrom):
#
#     nodelinks = [start[0]-1, start[1], start[2]]
#     noderechts = [start[0]+1, start[1], start[2]]
#     nodeboven = [start[0], start[1], start[2]+1]
#     nodebeneden = [start[0], start[1], start[2]-1]
#     nodevoor = [start[0], start[1] + 1, start[2]]
#     nodeachter = [start[0], start[1] - 1, start[2]]
#
#     # een niet gesloten node is groter dan 100 kleiner dan 10000
#     if check_isempty(nodelinks, grid) and checkexistance(nodelinks):
#      grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 100 + distance(locfrom, nodelinks) + distance(nodelinks, destination)
#
#      # een niet gesloten node is groter 10000
#     elif check_not_closed_node(nodelinks, grid) and checkexistance(nodelinks):
#      grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 10000 + distance(locfrom, nodelinks) + distance(nodelinks, destination)
#
#
#     if check_isempty(noderechts, grid) and checkexistance(noderechts):
#      grid[noderechts[0]][noderechts[1]][noderechts[2]] = 100 + distance(locfrom, noderechts) + distance(noderechts, destination)
#     elif check_not_closed_node(noderechts, grid) and checkexistance(noderechts):
#      grid[noderechts[0]][noderechts[1]][noderechts[2]] = 10000 + distance(locfrom, noderechts) + distance(noderechts, destination)
#
#
#     if check_isempty(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 100 + distance(locfrom, nodeboven) + distance(nodeboven, destination)
#     elif check_not_closed_node(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 10000 + distance(locfrom, nodeboven) + distance(nodeboven,
#                                                                                                   destination)
#
#     if check_isempty(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 100 + distance(locfrom, nodeboven) + distance(nodeboven, destination)
#     elif check_not_closed_node(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 10000 + distance(locfrom, nodeboven) + distance(nodeboven, destination)
#
#
#     if check_isempty(nodebeneden, grid) and checkexistance(nodebeneden):
#      grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 100 + distance(locfrom, nodebeneden) + distance(nodebeneden,
#                                                                                                   destination)
#     elif check_not_closed_node(nodebeneden, grid) and checkexistance(nodebeneden):
#      grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 10000 + distance(locfrom, nodebeneden) + distance(nodebeneden,
#                                                                                                   destination)
#
#
#     if check_isempty(nodevoor, grid) and checkexistance(nodevoor):
#      grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 100 + distance(locfrom, noderechts) + distance(noderechts,
#                                                                                                 destination)
#     elif check_not_closed_node(nodevoor, grid) and checkexistance(nodevoor):
#      grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 10000 + distance(locfrom, noderechts) + distance(noderechts,
#                                                                                                 destination)
#
#     if check_isempty(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 100 + distance(locfrom, nodeboven) + distance(nodeboven,
#                                                                                                     destination)
#     elif check_not_closed_node(nodeboven, grid) and checkexistance(nodeboven):
#      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 10000 + distance(locfrom, nodeboven) + distance(nodeboven,
#                                                                                                     destination)
#
#     if check_isempty(nodeachter, grid) and checkexistance(nodeachter):
#      grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = 100 + distance(locfrom, nodeachter) + distance(nodeachter,
#                                                                                                     destination)
#     elif check_not_closed_node(nodeachter, grid) and checkexistance(nodeachter):
#      grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = 10000 + distance(locfrom, nodeachter) + distance(nodeachter,
#                                                                                                  destination)
#     return grid
#
# # disntance berekenen tussen twee punten
#
# def distance(location, destination):
#     x_dist = abs(destination[0] - location[0])
#     y_dist = abs(destination[1] - location[1])
#     z_dist = abs(destination[2] - location[2])
#     distancee = z_dist + y_dist + x_dist
#     return distancee
#
# # kijken of de te plaatsen node zich wel in het veld bevindt
# def checkexistance(node):
#     if (node[2]<7 and node[2]>=0 and node[1]<18 and node[1]>=0 and node[0]>=0 and node[0]<13):
#         return True
#     else:
#         return False
#
# # als een element in matrix gelijk is aan 99 dan wordt is daar geen wire node of gate
#
# def check_isempty(node, grid):
#     if grid[node[0]][node[1]][node[2]] == 99:
#         return True
#     else:
#         return False
#
# # als een element groter is dan 100 is er node geplaatst
# def check_not_closed_node(node, grid):
#     if grid[node[0]][node[1]][node[2]] >= 100:
#         return True
#     else:
#         return False
#
# # node met laagste f cost is het nieuwe startpunt waaruit nodes geplaatst worden
# def minimumnodes(grid):
#     minimum = 10000
#     xvalue = 0
#     yvalue = 0
#     zvalue = 0
#     for x in range(13):
#         for y in range(18):
#             for z in range (7):
#                 if grid[x][y][z] < minimum and grid[x][y][z]>100:
#                     minimum = grid[x][y][z]
#                     xvalue = x
#                     yvalue = y
#                     zvalue = z
#
#     coordinates = [xvalue, yvalue , zvalue]
#     return coordinates
#
# # route wordt geplaatst, alle nodes zijn gegeven
# def findroute(gridwithnodes, locfrom, locto):
#     route = []
#     start = locto
#     while distance(start, locfrom) != 1:
#         routeelement = checkminimumclosednode(gridwithnodes, start)
#         route.append(routeelement)
#         start = routeelement
#
#     return route
#
# # closednode met laagste f cost, grenzend aan bepaald punt wordt bepaald
# def checkminimumclosednode(gridwithnodes, start):
#     minimum = 100000
#     minimumclosednode = [start[0]-1][start[1]][start[2]]
#     if checkexistance([start[0] - 1][start[1]][start[2]]) and 10000 < gridwithnodes[start[0] - 1][start[1]][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]-1][start[1]][start[2]]
#         minimumclosednode = [start[0]-1][start[1]][start[2]]
#
#     if checkexistance([start[0] + 1][start[1]][start[2]]) and 10000 < gridwithnodes[start[0] + 1][start[1]][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]+1][start[1]][start[2]]
#         minimumclosednode = [start[0]+1][start[1]][start[2]]
#
#     if checkexistance([start[0]][start[1] - 1][start[2]]) and 10000 < gridwithnodes[start[0]][start[1]-1][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]-1][start[2]]
#         minimumclosednode = [start[0]][start[1]-1][start[2]]
#
#     if checkexistance([start[0]][start[1] + 1][start[2]]) and 10000 < gridwithnodes[start[0]][start[1]+1][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]+1][start[2]]
#         minimumclosednode = [start[0]][start[1]+1][start[2]]
#
#     if checkexistance([start[0]][start[1]][start[2] - 1]) and 10000 < gridwithnodes[start[0]][start[1]][start[2]-1] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]][start[2]-1]
#         minimumclosednode = [start[0]][start[1]][start[2]-1]
#
#     if checkexistance([start[0]][start[1]][start[2] + 1]) and 10000 < gridwithnodes[start[0]][start[1]][start[2]+1] < minimum:
#         minimumclosednode = [start[0]][start[1]][start[2]+1]
#
#     return minimumclosednode
#
