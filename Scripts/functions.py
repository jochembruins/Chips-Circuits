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
from time import time
from typing import List

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from classes import *
from surroundings_gates import *
from random import randint
from random import shuffle
from copy import deepcopy
from surroundings_gates import *
import copy

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
        locFrom = [gates[point[0]].x, gates[point[0]].y, gates[point[0]].z]
        locTo = [gates[point[1]].x, gates[point[1]].y, gates[point[1]].z]
        # surrounding gridpoints of start/end point
        fromSurround = [[gates[point[0]].x, gates[point[0]].y + 1, gates[point[0]].z],
                      [gates[point[0]].x, gates[point[0]].y - 1, gates[point[0]].z],
                      [gates[point[0]].x + 1, gates[point[0]].y, gates[point[0]].z],
                      [gates[point[0]].x - 1, gates[point[0]].y, gates[point[0]].z ],
                      [gates[point[0]].x, gates[point[0]].y, gates[point[0]].z + 1]]
        toSurround = [[gates[point[1]].x, gates[point[1]].y + 1, gates[point[1]].z],
                      [gates[point[1]].x, gates[point[1]].y - 1, gates[point[1]].z],
                      [gates[point[1]].x + 1, gates[point[1]].y, gates[point[1]].z],
                      [gates[point[1]].x - 1, gates[point[1]].y, gates[point[1]].z],
                      [gates[point[1]].x, gates[point[1]].y, gates[point[1]].z +1]]
        route = []
        emptyRoute = wire(point, locFrom, locTo, fromSurround, toSurround, route)
        # print(emptyRoute)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def gridMat(gates):
    # make matrix of grid
    matgrid = np.zeros([18, 13, 15]) + 99

    for gate in gates:
        matgrid[gate.x, gate.y, gate.z] = gate.gate
    return matgrid


def randomRouteBook(routeBook, gates, steps=1000):
    random.seed(2)
    bestRouteBook = []

    score = 1000
    file  = open('random.csv', "w")
    writer = csv.writer(file, delimiter=',')
    
    for i in range(0, steps):
        print(i)
        newRouteBook = deepcopy(routeBook)

        shuffle(newRouteBook)

        grid = gridMat(gates)
        
        tmp_newRouteBook = deepcopy(newRouteBook)
        
        # checkt of het route vinden is gelukt
        finished = False
      
        newScore = score

        # if i == 14:
        #     for ding in newRouteBook:
        #         netlist12.append(ding.netPoint)
        #     print(netlist12)
        #     exit()
        
        # probeer nieuwe route te vinden
        try:
            newRouteFound = routeFinder(tmp_newRouteBook, grid)[1]

            finished = True
        except:
            finished = False



        # bereken nieuwe score   
        if finished:
            newScore = getScore(newRouteFound)
            print("oude score random: ", score)
            print("nieuwe score random: ", newScore)
            writer.writerow([i, newScore])
    
            
            check = checker(newRouteFound)

            if check == True:
                # sla score en route op als beste is
                if newScore < score:
                    bestRouteBook = deepcopy(newRouteBook)
                    bestRouteFound = deepcopy(newRouteFound)
                    score = newScore
                    print('lager')
                else:
                    print('hoger')

    file.close()
    return bestRouteBook, score, bestRouteFound



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
                if abs(locTo[1] - cursor[1]) > abs(locTo[0] - cursor[0]):
                    # step along y axis
                    if locTo[1] > cursor[1]:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1
                else:
                    # step along x axis
                    if locTo[0] > cursor[0]:
                        cursor[0] += 1
                    else:
                        cursor[0] -= 1
                # save step in route
                route.append([cursor[0], cursor[1], cursor[2]])

                # check if previous step is possible else delete and go up z-axis
                if grid[cursor[0], cursor[1], cursor[2]] != 99:

                    del route[-1]
                    cursor = [route[-1][0], route[-1][1], route[-1][2]]
                    cursor[2] += 1
                    route.append([cursor[0], cursor[1], cursor[2]])

                    # check if route has already been there when cursor up in previous step
                    if len(route) > 3 and route[-1] == route[-3]:
                        del route[-2:]

                    # if up not possible, cut wire above
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
                elif grid[cursor[0] , cursor[1], cursor[2] - 1] == 99.0 and cursor[2] > 0:
                    while grid[cursor[0] , cursor[1], cursor[2] - 1] == 99.0 and cursor[2] > 0:
                        cursor[2] -= 1
                        route.append([cursor[0], cursor[1], cursor[2]])

                # if above endpoint, go down and delete all blocking lines
                if [cursor[0], cursor[1]] == [locTo[0], locTo[1]]:
                    for netPointToDelete in routeBookDone:
                        for routepoint in netPointToDelete.route:
                            if [cursor[0], cursor[1], cursor[2] - 1] == [routepoint[0], routepoint[1], routepoint[2]]:
                                # remove line on grid
                                grid = delRoute(netPointToDelete.route[1:-1], grid)
                                netPointToDelete.route = []

                                # append deleted like back to the routebookempty list
                                routeBookEmpty.append(netPointToDelete)
                                del routeBookDone[routeBookDone.index(netPointToDelete)]
                                cursor[2] -= 1
                                route.append([cursor[0], cursor[1], cursor[2]])
                                break

                # delete first steps that are not usefull
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

            
            if count == 200:
                # print('meer dan 100')
                sys.exit


            for step in route:
                if step[2] > 10:
                    # print(netPoint)
                    # print(len(routeBookDone))
                    print('te hoog')
                    sys.exit
                    # return routeBookEmpty, routeBookDone, grid

            # save route in netPoint object
            netPoint.route = route

            # delete netPoint from to do list, append to done list
            doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
            routeBookDone.append(doneWire)


            # update matrix for route
            changeMat(netPoint.route[1:-1], grid)
    print(len(routeBookDone))
    for ding in routeBookDone:
        print(ding)

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
        ax.plot([step[0] for step in netPoint.route], [step[1] for step in netPoint.route], [step[2] for step in netPoint.route])

    plt.show()

def getScore(routeBook):
    score = 0
    for route in routeBook:
        score += (len(route.route) - 1)
    return score


def hillClimb(routeBook, score, gates, steps=1000):
    # maak variabele om beste route book op te slaan
    print('in Hillclimber')
    bestRouteBook = routeBook
    file  = open('hill.csv', "w")
    writer = csv.writer(file, delimiter=',')

    # loop voor het aantal stappen
    for i in range(0, steps):
        # maak lege grid
        grid = gridMat(gates)
        
        if i != 0:
            # verwissel willekeurig twee punten van de netlist
            newRouteBook = wire.changeRouteBook(bestRouteBook)
        else:
            print('same')
            newRouteBook = bestRouteBook
        
        tmp_newRouteBook = deepcopy(newRouteBook)  
        
        # checkt of het route vinden is gelukt
        finished = False
        # newScore = score
      
        # probeer nieuwe route te vinden
        try:
            newRouteFound = routeFinder(tmp_newRouteBook, grid)[1]
            finished = True
        except:
            finished = False

            
        # bereken nieuwe score   
        if finished: 
            newScore = getScore(newRouteFound)
            print("oude score: ", score)
            print("nieuwe score: ", newScore)
            
            check = checker(newRouteFound)

            if check == True:
                # sla score en route op als beste is
                if newScore <= score:
                    bestRouteBook = deepcopy(newRouteBook)
                    bestRouteFound = deepcopy(newRouteFound)
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
        print('check: goed')
        return True
    else:
        print('check: fout')
        print(repeated)
        return False

# hier begint het Astar algoritme met bijbehorende functies
# Astar returned uiteindelijk de wire/route van A*
# er wordt een matrix gedefinieerd waarbij de richtingen van nodes worden weergeven
def matrix_store_direction():
    # richtingen matrix geven
    # 1 links
    # 2 rechts
    # 3 boven
    # 4 beneden
    # 5 voor
    # 6 achter

    matgrid = np.zeros([18, 13, 8])
    return matgrid

def astarRouteFinder (routeBook, grid):
    routeBookAstarEmpty = deepcopy(routeBook)
    routeBookAstarDone = []
    j = 0
    
    while routeBookAstarEmpty != []:
        for netPoint in routeBookAstarEmpty:
            j += 1

            searchLocFrom(netPoint, routeBookAstarEmpty, routeBookAstarDone, grid)    
            searchLocTo(netPoint, routeBookAstarEmpty, routeBookAstarDone, grid)

            print(len(routeBookAstarEmpty))
            print(len(routeBookAstarDone))
            for route in routeBookAstarEmpty:
                print(route)

            # HIER ZIT HET PROBLEEM IN DE 47ste ITERATIE!
            route = Astar(netPoint, grid)
            
            if j == 47:
                print(netPoint)
                print(len(routeBookAstarEmpty))
                print(len(routeBookAstarDone))
                return routeBookAstarEmpty, routeBookAstarDone, grid

            netPoint.route = route
            grid = changeMat(route, grid)

            doneWire = routeBookAstarEmpty.pop(routeBookAstarEmpty.index(netPoint))
            routeBookAstarDone.append(doneWire)
            print(j)
            if j == 47:
                print(netPoint)
                print(len(routeBookAstarEmpty))
                print(len(routeBookAstarDone))
                return routeBookAstarEmpty, routeBookAstarDone, grid

    return routeBookAstarEmpty, routeBookAstarDone, grid


# Astar heeft een grid, gates en een wire nodig
def Astar(netPoint, emptyGrid):
    locfrom = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
    grid = deepcopy(emptyGrid)
    gridwithnodes = grid
    locto = [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]
    print("locfrom")
    print(locfrom)
    print("locto")
    print(locto)

    route=[]
    if distance(locfrom, locto) == 1:
        route.append(locto)
        route.append(locfrom)
    else:
        route = putwire(gridwithnodes, locfrom, locto)
        route.append(locfrom)
    route = list(reversed(route))

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

    nodelinkspotentieel = 1000000
    noderechtspotentieel = 1000000
    nodevoorpotentieel = 1000000
    nodeachterpotentieel = 1000000
    nodebovenpotentieel = 1000000
    nodebenedenpotentieel = 1000000

    # boven
    if checkexistance(nodeboven) and check_isempty(nodeboven, grid) and check_not_closed_node(nodeboven, grid):
        nodebovenpotentieel = 100 + Gcost(start, destination, grid, nodeboven) + distance(nodeboven, destination)

    if checkexistance(nodeboven) and (grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] == 99 or nodebovenpotentieel <
                                      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]):
        grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
        direction[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 3

    # beneden
    if checkexistance(nodebeneden) and check_isempty(nodebeneden, grid) and check_not_closed_node(nodebeneden, grid):
        nodebenedenpotentieel = 100 + Gcost(start, destination, grid, nodebeneden) + distance(nodebeneden, destination)

    if checkexistance(nodebeneden) and (
            grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] == 99 or nodebenedenpotentieel <
            grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]):
        grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
        direction[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 4

    # links
    if  checkexistance(nodelinks) and check_isempty(nodelinks, grid) and check_not_closed_node(nodelinks, grid):
        nodelinkspotentieel = 100 + Gcost(start, destination, grid, nodelinks) + distance(nodelinks, destination)


    if checkexistance(nodelinks) and (grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99 or nodelinkspotentieel < grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]):
        grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
        direction[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 1

    # rechts
    if checkexistance(noderechts) and check_isempty(noderechts, grid) and check_not_closed_node(noderechts, grid):
        noderechtspotentieel = 100 + Gcost(start, destination, grid, noderechts) + distance(noderechts, destination)


    if checkexistance(noderechts) and (grid[noderechts[0]][noderechts[1]][noderechts[2]] == 99 or noderechtspotentieel < grid[noderechts[0]][noderechts[1]][noderechts[2]]):
        grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
        direction[noderechts[0]][noderechts[1]][noderechts[2]] = 2


    # voor
    if checkexistance(nodevoor) and check_isempty(nodevoor, grid) and check_not_closed_node(nodevoor, grid):
        nodevoorpotentieel = 100 + Gcost(start, destination, grid, nodevoor) + distance(nodevoor, destination)

    if checkexistance(nodevoor) and (grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] == 99 or nodevoorpotentieel < grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]):
        grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
        direction[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 5

    # achter
    if checkexistance(nodeachter) and check_isempty(nodeachter, grid) and check_not_closed_node(nodeachter, grid):
        nodeachterpotentieel = 100 + Gcost(start, destination, grid, nodeachter) + distance(nodeachter, destination)

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
    if (node[2]<8 and node[2]>=0 and node[1]<13 and node[1]>=0 and node[0]>=0 and node[0]<18):
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
            for z in range (8):
                if grid[x][y][z] < minimum and grid[x][y][z]>100:
                    minimum = grid[x][y][z]
                    xvalue = x
                    yvalue = y
                    zvalue = z

    coordinates = [xvalue, yvalue , zvalue]
    return coordinates

# route wordt geplaatst, alle nodes zijn gegeven
def findroute(gridwithnodes, locfrom, locto, start, direction):
    index = 0
    route = []
    route.append(locto)
    route.append(start)
    while distance(locfrom, start) != 1:
        routeelement = checkclosednode(direction, start)
        route.append(routeelement)
        start = routeelement
    return route


def Gcost(start, destination, grid, node):
    if node in surround_list:

        count_surrounded = surround_list.count(node)
        if grid[start[0]][start[1]][start[2]] > 10000:
            gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1 + 10**count_surrounded
        else:
            gcost = 1 + 10**count_surrounded
        return gcost
    else:
        if grid[start[0]][start[1]][start[2]] > 10000:
            gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1
        else:
            gcost = 1
        return gcost


def checkclosednode(direction, start):
    value = direction[start[0]][start[1]][start[2]]

    # merk op dat de tegenovergestelde richting benodigd is
    if value == 1:
        start = [start[0] + 1, start[1], start[2]]

    elif value == 2:
        start = [start[0] - 1, start[1], start[2]]

    elif value == 3:
        start = [start[0], start[1], start[2] - 1]

    elif value == 4:
        start = [start[0], start[1], start[2] + 1]

    elif value == 5:
        start = [start[0], start[1] - 1, start[2]]

    elif value == 6:
        start = [start[0], start[1] + 1, start[2]]

    else:
        print("ERROR!!!")
        quit()
    return start


def getlistsurroundings(gates):
    list=[]
    for i in range(len(gates)):
        start = [gates[i].x, gates[i].y, gates[i].z]

        nodelinks = [start[0] - 1, start[1], start[2]]
        noderechts = [start[0] + 1, start[1], start[2]]
        nodeboven = [start[0], start[1], start[2] + 1]
        nodebeneden = [start[0], start[1], start[2] - 1]
        nodevoor = [start[0], start[1] + 1, start[2]]
        nodeachter = [start[0], start[1] - 1, start[2]]


        if checkexistance(nodelinks):
            list.append(nodelinks)
        if checkexistance(noderechts):
            list.append(noderechts)
        if checkexistance(nodeboven):
            list.append(nodeboven)
        if checkexistance(nodebeneden):
            list.append(nodebeneden)
        if checkexistance(nodevoor):
            list.append(nodevoor)
        if checkexistance(nodeachter):
            list.append(nodeachter)
    list=sorted(list)
    return list

def searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid):
    print('searchLocTo')
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
                        print(netPointToDelete)
                        del routeBookDone[routeBookDone.index(netPointToDelete)]
                        locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]

                        return routeBookEmpty, routeBookDone, grid

def searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid):
    print('searchLocFrom')
    for nextLocFrom in netPoint.fromSurround:
        for netPointToDelete in routeBookDone:
            for routepoint in netPointToDelete.route:
                if nextLocFrom == [routepoint[0], routepoint[1], routepoint[2]]:
                    if netPointToDelete.locTo != [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]] and \
                            netPointToDelete.locFrom != [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]] and \
                            nextLocFrom != netPointToDelete.locFrom:

                        # remove line on grid
                        grid = delRoute(netPointToDelete.route[1:-1], grid)
                        netPointToDelete.route = []

                        # append deleted line back to the routebookempty list

                        routeBookEmpty.append(netPointToDelete)
                        # delete line from routebookdone list
                        print(netPointToDelete)
                        del routeBookDone[routeBookDone.index(netPointToDelete)]
                        locFrom = [nextLocFrom[0], nextLocFrom[1], nextLocFrom[2]]

                        return routeBookEmpty, routeBookDone, grid

