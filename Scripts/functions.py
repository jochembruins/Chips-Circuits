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

import csv
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
    matgrid = np.zeros([20, 13, 18]) + 99

    for gate in gates:
        matgrid[gate.z, gate.y, gate.x] = gate.gate
    return matgrid


def routeFinder(routeBook, grid):
    routeBookEmpty = routeBook
    routeBookDone = []
    count = 0
    while routeBookEmpty != []:
        for netPoint in routeBookEmpty:
            stop = 0
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

                    if grid[cursor[0], cursor[1], cursor[2]] != 99:
                        for netPointToDelete in routeBookDone:
                            for routepoint in netPointToDelete.route:
                                if [cursor[0], cursor[1], cursor[2]] == [routepoint[0], routepoint[1], routepoint[2]]:
                                    # remove line on grid
                                    grid = delRoute(netPointToDelete.route[1:-1], grid)
                                    netPointToDelete.route = []

                                    # append deleted like back to the routebookempty list
                                    routeBookEmpty.append(netPointToDelete)
                                    del routeBookDone[routeBookDone.index(netPointToDelete)]
                                    break

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
                # delete useless first steps
                if len(route) > 2 and abs(netPoint.locFrom[0] - cursor[0]) + abs(netPoint.locFrom[1] - cursor[1]) + abs(netPoint.locFrom[2] - cursor[2]) == 1:
                    del route[-3:-1]
                # if only one step away from original endpoint, stop
                if abs(netPoint.locTo[0] - cursor[0]) + abs(netPoint.locTo[1] - cursor[1]) + abs(netPoint.locTo[2] - cursor[2]) < 2:
                    stop = 1
                    break

            # add end point to route
            if stop == 0:
                route.append(locTo)
            route.append(netPoint.locTo)
            count +=1
            
            if count == 100:
                sys.exit

            for step in route:
                if step[0] > 7:
                    sys.exit

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
    # maak variabele om beste route book op te slaan
    bestRouteBook = routeBook
    file  = open('hill.csv', "w")
    writer = csv.writer(file, delimiter=',')

    # loop voor het aantal stappen
    for i in range(0, steps):
        print(i)
        # maak lege grid
        grid = gridMat(gates)
        
        # verwissel willekeurig twee punten van de netlist
        newRouteBook = wire.changeRouteBook(bestRouteBook)
        
        tmp_newRouteBook = deepcopy(newRouteBook)  
        
        # scorevariabele op inganspunt stellen
        newScore = score
        
        # checkt of het route vinden is gelukt
        finished = False
      
        # probeer nieuwe route te vinden
        try:
            newRouteFound = routeFinder(tmp_newRouteBook, grid)[1]
            finished = True
        except:
            finished = False

            
        # bereken nieuwe score   
        if finished: 
            newScore = getScore(newRouteFound)
            print(score)
            print(newScore)
            
            check = checker(newRouteFound)

            if check == True:
                # sla score en route op als beste is
                if newScore < score:
                    bestRouteBook = newRouteBook
                    bestRouteFound = newRouteFound
                    score = newScore
                    print('lager')
                else:
                    print('hoger')
        
        
        writer.writerow([i,score])
    file.close()
    return bestRouteFound, score


def checker (routeBook):
    seen = []
    repeated = []

    for route in routeBook:
      for step in route.route[1:-1]:
        if step in seen:
          repeated.append(step)
        else:
          seen.append(step)

    if len(repeated) == 0:
        return True
    else:
        print(repeated)
        return False




# hier begint het Astar algoritme met bijbehorende functies
# 

# Astar(,grid)
# Astar returned uiteindelijk de wire/route van A*


# def gridMat2(gates):
#     # make matrix of grid
#     matgrid = np.zeros([18, 13, 7]) + 99
#
#     for gate in gates:
#         matgrid[gate.x, gate.y, gate.z] = gate.gate
#     return matgrid
#
# def Astar(gates, wire, grid):
#     locfrom = [gates[wire[0]].x, gates[wire[0]].y, gates[wire[0]].z]
#     gridwithnodes = grid
#     locto = [gates[wire[1]].x, gates[wire[1]].y, gates[wire[1]].z]
#     print("locfrom")
#     print(locfrom)
#     print("locto")
#     print(locto)

#     route = putwire(gridwithnodes, locfrom, locto)
#     return route
#
# # putwire plaatst nodes totdat de locatie bereikt is
# def putwire(gridwithnodes, locfrom, locto):
#     start = locfrom

#     listclosednodes=[]
#     while (distance(start, locto) != 1):
#         gridwithnodes = putnodes(start, gridwithnodes, locto, locfrom)
#         listclosednodes.append()
#         start = minimumnodes(gridwithnodes)
#
#     print("man man man")
#     for x in range(18):
#         for y in range(13):
#             for z in range(7):
#                 if gridwithnodes[x][y][z] >= 10000 :
#                     print("x: ", end='')
#                     print(x, end='')
#                     print(" y: ", end='')
#                     print(y, end='')
#                     print(" z: ", end='')
#                     print(z, end='')
#                     print(" grid: ", end='')
#                     print(gridwithnodes[x][y][z])
#
#     print("man man man")
#
#     route = findroute(gridwithnodes, locfrom, locto, start)
#     while (distance(start, locto) != 1):
#         gridwithnodes = putnodes(start, gridwithnodes, locto, locfrom)
#         start = minimumnodes(gridwithnodes)
#     route = findroute(gridwithnodes, locfrom, locto)
#     return route
#
# #  nodes plaatsen
# def putnodes(start, grid, destination, locfrom):
#     if grid[start[0]][start[1]][start[2]] >= 100:
#
#         # een  gesloten node is groter dan 10000
#         grid[start[0]][start[1]][start[2]] = 10000 - 100 + grid[start[0]][start[1]][start[2]]
#
#     nodelinks = [start[0]-1, start[1], start[2]]
#     noderechts = [start[0]+1, start[1], start[2]]
#     nodeboven = [start[0], start[1], start[2]+1]
#     nodebeneden = [start[0], start[1], start[2]-1]
#     nodevoor = [start[0], start[1] + 1, start[2]]
#     nodeachter = [start[0], start[1] - 1, start[2]]
#

#     #
#     # node kan alleen geclosed worden als er vanuit die node gekeken wordt
#     #
#     #
#
#     # een niet gesloten node is groter dan 100 kleiner dan 10000
#
#
#     nodelinkspotentieel = 1000000
#     noderechtspotentieel = 1000000
#     nodevoorpotentieel = 1000000
#     nodeachterpotentieel = 1000000
#     nodebovenpotentieel = 1000000
#     nodebenedenpotentieel = 1000000
#
#
#     # links
#     if check_isempty(nodelinks, grid) and checkexistance(nodelinks) and check_not_closed_node(nodelinks, grid):
#         nodelinkspotentieel = 100 + Gcost(start, destination, grid) + distance(nodelinks, destination)
#
#     if checkexistance(nodelinks) and (grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99 or nodelinkspotentieel < grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]):
#         grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
#
#     # rechts
#     if check_isempty(noderechts, grid) and checkexistance(noderechts) and check_not_closed_node(noderechts, grid):
#         noderechtspotentieel = 100 + Gcost(start, destination, grid) + distance(noderechts, destination)
#
#
#     if checkexistance(noderechts) and (grid[noderechts[0]][noderechts[1]][noderechts[2]] == 99 or noderechtspotentieel < grid[noderechts[0]][noderechts[1]][noderechts[2]]):
#         grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
#
#     # boven
#     if check_isempty(nodeboven, grid) and checkexistance(nodeboven) and check_not_closed_node(nodeboven, grid):
#         nodebovenpotentieel = 100 + Gcost(start, destination, grid) + distance(nodeboven, destination)
#
#     if checkexistance(nodeboven) and (grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] == 99 or nodebovenpotentieel < grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]):
#         grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
#
#     # beneden
#     if check_isempty(nodebeneden, grid) and checkexistance(nodebeneden) and check_not_closed_node(nodebeneden, grid):
#         nodebenedenpotentieel = 100 + Gcost(start, destination, grid) + distance(nodebeneden, destination)
#
#     if checkexistance(nodebeneden) and (grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] == 99 or nodebenedenpotentieel < grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]):
#         grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
#
#     # voor
#     if check_isempty(nodevoor, grid) and checkexistance(nodevoor) and check_not_closed_node(nodevoor, grid):
#         nodevoorpotentieel = 100 + Gcost(start, destination, grid) + distance(nodevoor, destination)
#
#     if checkexistance(nodevoor) and (grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] == 99 or nodevoorpotentieel < grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]):
#         grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
#
#
#     # achter
#     if check_isempty(nodeachter, grid) and checkexistance(nodeachter) and check_not_closed_node(nodeachter, grid):
#         nodeachterpotentieel = 100 + Gcost(start, destination, grid) + distance(nodeachter, destination)
#
#     if checkexistance(nodeachter) and (grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] == 99 or nodeachterpotentieel < grid[nodeachter[0]][nodeachter[1]][nodeachter[2]]):
#         grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = nodeachterpotentieel
#
#     # print("man man man")
#     # for x in range(18):
#     #     for y in range(13):
#     #         for z in range(7):
#     #             if grid[x][y][0] != 99:
#     #                 print("x: ", end='')
#     #                 print(x, end='')
#     #                 print(" y: ", end='')
#     #                 print(y, end='')
#     #                 print(" z: ", end='')
#     #                 print(z, end='')
#     #                 print(" grid: ", end='')
#     #                 print(grid[x][y][z])
#     #
#     # print("man man man")
#     # quit()

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
#     if (node[2]<7 and node[2]>=0 and node[1]<13 and node[1]>=0 and node[0]>=0 and node[0]<18):
#     if (node[2]<7 and node[2]>=0 and node[1]<18 and node[1]>=0 and node[0]>=0 and node[0]<13):
#         return True
#     else:
#         return False
#
# # als een element in matrix gelijk is aan 99 dan wordt is daar geen wire node of gate
#
# def check_isempty(node, grid):
#     if grid[node[0]][node[1]][node[2]] >= 99 and grid[node[0]][node[1]][node[2]]<10000:
#     if grid[node[0]][node[1]][node[2]] == 99:
#         return True
#     else:
#         return False
#
# # als een element groter is dan 100 is er node geplaatst
# def check_not_closed_node(node, grid):
#     if grid[node[0]][node[1]][node[2]] >= 100:
#         return False
#     else:
#         return True
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
#     for x in range(18):
#         for y in range(13):
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
# def findroute(gridwithnodes, locfrom, locto, start):
#     index = 0
#     route = []
#     route.append(start)
#     while distance(locfrom, start) != 1:
#         routeelement = checkminimumclosednode(gridwithnodes, locfrom)
#         route.append(routeelement)
#         locfrom = routeelement
#         print("locfrom")
#         print(locfrom)
#         index = index + 1
#         if index>20:
#             quit()
#     route.append(start)

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

# def checkminimumclosednode(gridwithnodes, start):
#     minimum = 1000000
#     minimumclosednode = [start[0], start[1], start[2]]
#     if checkexistance([start[0] - 1, start[1], start[2]]) and 10000 < gridwithnodes[start[0] - 1][start[1]][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]-1][start[1]][start[2]]
#         minimumclosednode = [start[0]-1, start[1], start[2]]
#
#     if checkexistance([start[0] + 1, start[1], start[2]]) and 10000 < gridwithnodes[start[0] + 1][start[1]][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]+1][start[1]][start[2]]
#         minimumclosednode = [start[0]+1, start[1], start[2]]
#
#     if checkexistance([start[0], start[1]-1, start[2]]) and 10000 < gridwithnodes[start[0]][start[1]-1][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]-1][start[2]]
#         minimumclosednode = [start[0], start[1]-1, start[2]]
#
#     if checkexistance([start[0], start[1]+1, start[2]]) and 10000 < gridwithnodes[start[0]][start[1]+1][start[2]] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]+1][start[2]]
#         minimumclosednode = [start[0], start[1]+1, start[2]]
#
#     if checkexistance([start[0], start[1], start[2]-1]) and 10000 < gridwithnodes[start[0]][start[1]][start[2]-1] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]][start[2]-1]
#         minimumclosednode = [start[0], start[1], start[2]-1]
#
#     if checkexistance([start[0], start[1], start[2]+1]) and 10000 < gridwithnodes[start[0]][start[1]][start[2]+1] < minimum:
#         minimum = gridwithnodes[start[0]][start[1]][start[2]+1]
#         minimumclosednode = [start[0], start[1], start[2]+1]
#
#     return minimumclosednode
#
# def Gcost(start, destination, grid):
#     if grid[start[0]][start[1]][start[2]]>10000:
#         gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1
#     else:
#         gcost = 1
#     return gcost



# hier begint het Astar algoritme met bijbehorende functies


# Astar(,grid)
# Astar returned uiteindelijk de wire/route van A*

def gridMat2(gates):
    # make matrix of grid
    matgrid = np.zeros([18, 13, 7]) + 99

    for gate in gates:
        matgrid[gate.x, gate.y, gate.z] = gate.gate
    return matgrid

def matrix_store_direction():
    # richtingen matrix geven
    # 1 links
    # 2 rechts
    # 3 boven
    # 4 beneden
    # 5 voor
    # 6 achter

    matgrid = np.zeros([18, 13, 7])
    return matgrid
def hulp(matrix_store_direction):
    matrix_store_direction[0][0][0] = "right"
    return matrix_store_direction


def Astar(gates, wire, grid):
    locfrom = [gates[wire[0]].x, gates[wire[0]].y, gates[wire[0]].z]
    gridwithnodes = grid
    locto = [gates[wire[1]].x, gates[wire[1]].y, gates[wire[1]].z]
    print("locfrom")
    print(locfrom)
    print("locto")
    print(locto)
    route = putwire(gridwithnodes, locfrom, locto)
    return route

# putwire plaatst nodes totdat de locatie bereikt is
def putwire(gridwithnodes, locfrom, locto):
    start = locfrom
    direction = matrix_store_direction()
    while (distance(start, locto) != 1):
        gridwithnodes = putnodes(start, gridwithnodes, locto, locfrom, direction)[0]
        direction = putnodes(start, gridwithnodes, locto, locfrom, direction)[1]
        start = minimumnodes(gridwithnodes)

    route = findroute(gridwithnodes, locfrom, locto, start, direction)
    return route

#  nodes plaatsen
def putnodes(start, grid, destination, locfrom, direction):
    if grid[start[0]][start[1]][start[2]] >= 100:

        # een  gesloten node is groter dan 10000
        grid[start[0]][start[1]][start[2]] = 10000 - 100 + grid[start[0]][start[1]][start[2]]

    nodelinks = [start[0]-1, start[1], start[2]]
    noderechts = [start[0]+1, start[1], start[2]]
    nodeboven = [start[0], start[1], start[2]+1]
    nodebeneden = [start[0], start[1], start[2]-1]
    nodevoor = [start[0], start[1] + 1, start[2]]
    nodeachter = [start[0], start[1] - 1, start[2]]

    #
    # node kan alleen geclosed worden als er vanuit die node gekeken wordt
    #
    #

    # een niet gesloten node is groter dan 100 kleiner dan 10000


    nodelinkspotentieel = 1000000
    noderechtspotentieel = 1000000
    nodevoorpotentieel = 1000000
    nodeachterpotentieel = 1000000
    nodebovenpotentieel = 1000000
    nodebenedenpotentieel = 1000000


    # links
    if check_isempty(nodelinks, grid) and checkexistance(nodelinks) and check_not_closed_node(nodelinks, grid):
        nodelinkspotentieel = 100 + Gcost(start, destination, grid) + distance(nodelinks, destination)


    if checkexistance(nodelinks) and (grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99 or nodelinkspotentieel < grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]):
        grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
        direction[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 1

    # rechts
    if check_isempty(noderechts, grid) and checkexistance(noderechts) and check_not_closed_node(noderechts, grid):
        noderechtspotentieel = 100 + Gcost(start, destination, grid) + distance(noderechts, destination)


    if checkexistance(noderechts) and (grid[noderechts[0]][noderechts[1]][noderechts[2]] == 99 or noderechtspotentieel < grid[noderechts[0]][noderechts[1]][noderechts[2]]):
        grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
        direction[noderechts[0]][noderechts[1]][noderechts[2]] = 2

    # boven
    if check_isempty(nodeboven, grid) and checkexistance(nodeboven) and check_not_closed_node(nodeboven, grid):
        nodebovenpotentieel = 100 + Gcost(start, destination, grid) + distance(nodeboven, destination)


    if checkexistance(nodeboven) and (grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] == 99 or nodebovenpotentieel < grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]):
        grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
        direction[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 3

    # beneden
    if check_isempty(nodebeneden, grid) and checkexistance(nodebeneden) and check_not_closed_node(nodebeneden, grid):
        nodebenedenpotentieel = 100 + Gcost(start, destination, grid) + distance(nodebeneden, destination)

    if checkexistance(nodebeneden) and (grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] == 99 or nodebenedenpotentieel < grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]):
        grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
        direction[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 4

    # voor
    if check_isempty(nodevoor, grid) and checkexistance(nodevoor) and check_not_closed_node(nodevoor, grid):
        nodevoorpotentieel = 100 + Gcost(start, destination, grid) + distance(nodevoor, destination)

    if checkexistance(nodevoor) and (grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] == 99 or nodevoorpotentieel < grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]):
        grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
        direction[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 5


    # achter
    if check_isempty(nodeachter, grid) and checkexistance(nodeachter) and check_not_closed_node(nodeachter, grid):
        nodeachterpotentieel = 100 + Gcost(start, destination, grid) + distance(nodeachter, destination)

    if checkexistance(nodeachter) and (grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] == 99 or nodeachterpotentieel < grid[nodeachter[0]][nodeachter[1]][nodeachter[2]]):
        grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = nodeachterpotentieel
        direction[nodeachter[0]][nodeachter[1]][nodeachter[2]] = 6


    return grid, direction


# disntance berekenen tussen twee punten

def distance(location, destination):
    x_dist = abs(destination[0] - location[0])
    y_dist = abs(destination[1] - location[1])
    z_dist = abs(destination[2] - location[2])
    distancee = z_dist + y_dist + x_dist
    return distancee

# kijken of de te plaatsen node zich wel in het veld bevindt
def checkexistance(node):
    if (node[2]<7 and node[2]>=0 and node[1]<13 and node[1]>=0 and node[0]>=0 and node[0]<18):
        return True
    else:
        return False

# als een element in matrix gelijk is aan 99 dan wordt is daar geen wire node of gate

def check_isempty(node, grid):
    if grid[node[0]][node[1]][node[2]] >= 99 and grid[node[0]][node[1]][node[2]]<10000:
        return True
    else:
        return False

# als een element groter is dan 100 is er node geplaatst
def check_not_closed_node(node, grid):
    if grid[node[0]][node[1]][node[2]] >= 100:
        return False
    else:
        return True

# node met laagste f cost is het nieuwe startpunt waaruit nodes geplaatst worden
def minimumnodes(grid):
    minimum = 10000
    xvalue = 0
    yvalue = 0
    zvalue = 0
    for x in range(18):
        for y in range(13):
            for z in range (7):
                if grid[x][y][z] < minimum and grid[x][y][z]>100:
                    minimum = grid[x][y][z]
                    xvalue = x
                    yvalue = y
                    zvalue = z

    coordinates = [xvalue, yvalue , zvalue]
    return coordinates

# route wordt geplaatst, alle nodes zijn gegeven
def findroute(gridwithnodes, locfrom, locto, start, direction):
    route = []
    route.append(start)
    print("hoi allalalalallalalal")
    print(locfrom)
    print(start)
    while distance(locfrom, start) != 1:
        print("erin")
        routeelement = checkclosednode(direction, start)
        route.append(routeelement)
        start = routeelement
    route.append(start)
    return route


def Gcost(start, destination, grid):
    if grid[start[0]][start[1]][start[2]]>10000:
        gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1
    else:
        gcost = 1
    return gcost

def checkclosednode(direction, locfrom):
    value = direction[locfrom[0]][locfrom[1]][locfrom[2]]

    if value == 1:
        locfrom = [locfrom[0] - 1, locfrom[1], locfrom[2]]

    elif value == 2:
        locfrom = [locfrom[0] + 1, locfrom[1], locfrom[2]]

    elif value == 3:
        locfrom = [locfrom[0], locfrom[1], locfrom[2] + 1]

    elif value == 4:
        locfrom = [locfrom[0], locfrom[1], locfrom[2] - 1]

    elif value == 5:
        locfrom = [locfrom[0], locfrom[1] + 1, locfrom[2]]

    elif value == 6:
        locfrom = [locfrom[0], locfrom[1] - 1, locfrom[2]]

    return locfrom
