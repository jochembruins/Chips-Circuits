# python script
###########################################################
# functions.py
#
# Jochem Bruins
# 10578811
#
# Melle Gelok
# 11017893
#
# Noah van Grinsven
# 10501917
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
import classes
from random import randint
import random
from random import shuffle
from copy import deepcopy
from surroundings_gates import surround_list

np.set_printoptions(threshold=np.nan)
np.set_printoptions(linewidth=180)


def makeLocations(data):
    gates = []
    for line in data:
        line = classes.Location(line[0], int(line[1]), int(line[2]), int(line[3]))
        gates.append(line)
    return gates


def makeObjects(netlist, gates):
    emptyRouteBook = []

    for point in netlist:
        locFrom = [gates[point[0]].x, gates[point[0]].y, gates[point[0]].z]
        locTo = [gates[point[1]].x, gates[point[1]].y, gates[point[1]].z]
        # omliggende punten van begin/eindpunt
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
        emptyRoute = classes.wire(point, locFrom, locTo, fromSurround, toSurround, route)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def gridMat(gates):
    # make matrix of grid
    matgrid = np.zeros([18, 17, 10]) + 99

    for gate in gates:
        matGrid[gate.x, gate.y, gate.z] = gate.gate
    return matGrid


def randomRouteBook(routeBook, gates, steps=1000):

    random.seed(2)
    bestRouteBook = []

    score = 2000
    file  = open('../csv/random.csv', "w")
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
                    print('betere oplossing')
                else:
                    print('slechtere oplossing')
            else:
                for ding in newRouteFound:
                    print(ding)

    file.close()
    return bestRouteBook, score, bestRouteFound, grid


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

            if stepsDifference(locTo, cursor) != 1:
                # select which gridpoint next to end location is free
                for nextLocTo in netPoint.toSurround:
                    if grid[nextLocTo[0], nextLocTo[1], nextLocTo[2]] == 99:
                        locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]
                        break

                # if end location cant be reached, delete one of lines on surrounding gridpoints
                if locTo == [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]:
                    routeBookEmpty, routeBookDone, grid, locTo = searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid)

                # make first step in available direction
                for nextLocFrom in netPoint.fromSurround:
                    if grid[nextLocFrom[0], nextLocFrom[1], nextLocFrom[2]] == 99:
                        cursor = [nextLocFrom[0], nextLocFrom[1], nextLocFrom[2]]
                        route.append([cursor[0], cursor[1], cursor[2]])
                        break

                # if there is no valid first step possible, delete one of lines on surrounding gridpoints
                if cursor == [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]:
                    routeBookEmpty, routeBookDone, grid, [cursor[0], cursor[1], cursor[2]] = searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid)
                    route.append([cursor[0], cursor[1], cursor[2]])


            # look for best step until 1 step away from endpoint
            while stepsDifference(locTo, cursor) > 1:
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

                # delete steps if route has already been there
                if len(route) > 3 and route[-1] == route[-3]:
                    del route[-2:]
                if len(route) > 4 and route[-1] == route[-5]:
                    del route[-4:]

                # check if previous step is possible else delete step and go up z-axis
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
                            for routePoint in netPointToDelete.route:
                                if [cursor[0], cursor[1], cursor[2]] == [routePoint[0], routePoint[1], routePoint[2]]:
                                    # remove line on grid
                                    grid = delRoute(netPointToDelete.route, grid)
                                    netPointToDelete.route = []

                                    # append deleted like back to the routebookempty list
                                    routeBookEmpty.append(netPointToDelete)
                                    del routeBookDone[routeBookDone.index(netPointToDelete)]
                                    break

                # if step down is possible, go down
                elif grid[cursor[0], cursor[1], cursor[2] - 1] == 99.0 and cursor[2] > locTo[2]:
                    while grid[cursor[0], cursor[1], cursor[2] - 1] == 99.0 and cursor[2] > locTo[2]:
                        cursor[2] -= 1
                        route.append([cursor[0], cursor[1], cursor[2]])

                        # check if route has already been there when cursor up in previous step
                        if len(route) > 3 and route[-1] == route[-3]:
                            del route[-2:]

                # if above endpoint, go down and delete all blocking lines
                if [cursor[0], cursor[1]] == [locTo[0], locTo[1]] and cursor[2] != locTo[2]:
                    # find lines that are beneath cursor
                    for netPointToDelete in routeBookDone:
                        for routePoint in netPointToDelete.route:
                            if [cursor[0], cursor[1], cursor[2] - 1] == [routePoint[0], routePoint[1], routePoint[2]]:
                                # remove line on grid
                                grid = delRoute(netPointToDelete.route, grid)
                                netPointToDelete.route = []

                                # append deleted like back to the routebookempty list
                                routeBookEmpty.append(netPointToDelete)
                                del routeBookDone[routeBookDone.index(netPointToDelete)]
                                cursor[2] -= 1

                                route.append([cursor[0], cursor[1], cursor[2]])
                                break

                # delete first steps that are not useful
                if len(route) > 2 and stepsDifference(netPoint.locFrom, cursor) == 1:
                    del route[1:len(route) - 1]
                # if only one step away from original endpoint, stop
                if stepsDifference(netPoint.locTo, cursor) == 1:
                    break

            # add end point to route
            if stepsDifference(netPoint.locTo, cursor) != 1:
                route.append(locTo)
            route.append(netPoint.locTo)
            count += 1

            if count == 150:
                # print('meer dan 150')
                sys.exit


            for step in route:
                if step[2] > 29:
                    # print('te hoog')
                    sys.exit

            # save route in netPoint object
            netPoint.route = route

            # delete netPoint from to empty list, append to done list
            doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
            routeBookDone.append(doneWire)


            # update matrix for route
            changeMat(netPoint.route, grid)

    return routeBookEmpty, routeBookDone, grid

def changeMat(route, grid):
    for step in route[1:-1]:
        grid[step[0], step[1], step[2]] = 50
    return grid

def delRoute(route, grid):
    for step in route[1:-1]:
        grid[step[0], step[1], step[2]] = 99
    return grid

def stepsDifference(vector1, vector2):
    difference = abs(vector1[0] - vector2[0]) + abs(vector1[1] - vector2[1]) + abs(vector1[2] - vector2[2])
    return difference


def plotLines(gates, routeBook):
    # maak een nieuwe plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # definieer assen
    ax.set_xlim([0, 18])
    ax.set_ylim([0, 17])
    ax.set_zlim([0, 10])

    # zet ticks op de assem
    ax.set_xticks(np.arange(0, 18, 1))
    ax.set_yticks(np.arange(0, 17, 1))
    ax.set_zticks(np.arange(0, 10, 1))

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
    file  = open('../csv/hill.csv', "w")
    writer = csv.writer(file, delimiter=',')

    # loop voor het aantal stappen
    for i in range(0, steps):
        # maak lege grid
        grid = gridMat(gates)
        
        if i != 0:
            # verwissel willekeurig twee punten van de netlist
            newRouteBook = classes.wire.changeRouteBook(bestRouteBook)
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

    matgrid = np.zeros([18, 17, 10])
    return matgrid

def astarRouteFinder (routeBook, grid):

    gridEmpty = deepcopy(grid)
    routeBookAstarEmpty = deepcopy(routeBook)
    routeBookAstarDone = []
    loops = 0

    while routeBookAstarEmpty != []:
        for netPoint in routeBookAstarEmpty:
            
            loops += 1

            count = 0
            for loc in netPoint.fromSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            if count == 5:
                routeBookAstarEmpty, routeBookAstarDone, grid = searchLocFrom(netPoint, routeBookAstarEmpty, routeBookAstarDone, grid)   

            count = 0
            for loc in netPoint.toSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            if count == 5:
                routeBookAstarEmpty, routeBookAstarDone, grid = searchLocTo(netPoint, routeBookAstarEmpty, routeBookAstarDone, grid)         


            print(len(routeBookAstarEmpty))
            print(len(routeBookAstarDone))

            route = Astar(netPoint, grid, 2)

            if route != []:
                netPoint.route = route
                grid = changeMat(route, grid)

                doneWire = routeBookAstarEmpty.pop(routeBookAstarEmpty.index(netPoint))
                routeBookAstarDone.append(doneWire)
            
            if loops == 100:
                routeBookAstarEmpty = routeBookAstarEmpty + routeBookAstarDone
                routeBookAstarDone = []
                shuffle(routeBookAstarEmpty)
                grid = deepcopy(gridEmpty)
                loops = 0

    print("Returning: ")
    return routeBookAstarDone


# Astar heeft een grid, gates en een wire nodig
def Astar(netPoint, grid, index):
    locfrom = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
    gridwithnodes = deepcopy(emptyGrid)
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
        route = putwire(gridwithnodes, locfrom, locto, index)
        if route != []:
            route.append(locfrom)
    route = list(reversed(route))

    return route

# putwire plaatst nodes totdat de locatie bereikt is
def putwire(gridwithnodes, locfrom, locto, index):
    start = locfrom
    direction = matrix_store_direction()
    stop = 0

    while (distance(start, locto) != 1) and stop == 0:
        gridwithnodes = putnodes(start, gridwithnodes, locto, locfrom, direction, index)[0]
        direction = putnodes(start, gridwithnodes, locto, locfrom, direction, index)[1]

        start = minimumnodes(gridwithnodes)[0]
        stop = minimumnodes(gridwithnodes)[1]

    if stop == 0:
        route = findroute(gridwithnodes, locfrom, locto, start, direction)
    else:

        route=[]
        print("mislukt:")
        print(locfrom)
        print(locto)
        print("mislukt eindig")
    return route

#  nodes plaatsen
def putnodes(start, grid, destination, locfrom, direction, index):
    if grid[start[0]][start[1]][start[2]] >= 100:

        # een  gesloten node is groter dan 10000
        grid[start[0]][start[1]][start[2]] = 10000 - 100 + grid[start[0]][start[1]][start[2]]

    nodelinks = [start[0]-1, start[1], start[2]]
    noderechts = [start[0]+1, start[1], start[2]]
    nodeboven = [start[0], start[1], start[2]+1]
    nodebeneden = [start[0], start[1], start[2]-1]
    nodevoor = [start[0], start[1] + 1, start[2]]
    nodeachter = [start[0], start[1] - 1, start[2]]

    # print("hoi")
    # if not checkexistance(nodeboven) or not check_isempty(nodeboven, grid) and \
    # not checkexistance(nodebeneden) or not check_isempty(nodebeneden, grid) and \
    # not checkexistance(nodevoor) or not check_isempty(nodevoor, grid) and \
    # not checkexistance(nodeachter) or not check_isempty(nodeachter, grid) and \
    # not checkexistance(nodelinks) or not check_isempty(nodelinks, grid) and \
    # not checkexistance(noderechts) or not check_isempty(noderechts, grid):
    #     quit()


    nodelinkspotentieel = 1000000
    noderechtspotentieel = 1000000
    nodevoorpotentieel = 1000000
    nodeachterpotentieel = 1000000
    nodebovenpotentieel = 1000000
    nodebenedenpotentieel = 1000000

    # boven
    if checkexistance(nodeboven) and check_isempty(nodeboven, grid) and check_not_closed_node(nodeboven, grid):
        nodebovenpotentieel = 100 + Gcost(start, destination, grid, nodeboven, index) + distance(nodeboven, destination)

    if checkexistance(nodeboven) and (grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] == 99 or nodebovenpotentieel <
                                      grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]):
        grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
        direction[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 3

    # beneden
    if checkexistance(nodebeneden) and check_isempty(nodebeneden, grid) and check_not_closed_node(nodebeneden, grid):
        nodebenedenpotentieel = 100 + Gcost(start, destination, grid, nodebeneden, index) + distance(nodebeneden, destination)

    if checkexistance(nodebeneden) and (
            grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] == 99 or nodebenedenpotentieel <
            grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]):
        grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
        direction[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 4

    # links
    if  checkexistance(nodelinks) and check_isempty(nodelinks, grid) and check_not_closed_node(nodelinks, grid):
        nodelinkspotentieel = 100 + Gcost(start, destination, grid, nodelinks, index) + distance(nodelinks, destination)


    if checkexistance(nodelinks) and (grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99 or nodelinkspotentieel < grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]):
        grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
        direction[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 1

    # rechts
    if checkexistance(noderechts) and check_isempty(noderechts, grid) and check_not_closed_node(noderechts, grid):
        noderechtspotentieel = 100 + Gcost(start, destination, grid, noderechts, index) + distance(noderechts, destination)


    if checkexistance(noderechts) and (grid[noderechts[0]][noderechts[1]][noderechts[2]] == 99 or noderechtspotentieel < grid[noderechts[0]][noderechts[1]][noderechts[2]]):
        grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
        direction[noderechts[0]][noderechts[1]][noderechts[2]] = 2


    # voor
    if checkexistance(nodevoor) and check_isempty(nodevoor, grid) and check_not_closed_node(nodevoor, grid):
        nodevoorpotentieel = 100 + Gcost(start, destination, grid, nodevoor, index) + distance(nodevoor, destination)

    if checkexistance(nodevoor) and (grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] == 99 or nodevoorpotentieel < grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]):
        grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
        direction[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 5

    # achter
    if checkexistance(nodeachter) and check_isempty(nodeachter, grid) and check_not_closed_node(nodeachter, grid):
        nodeachterpotentieel = 100 + Gcost(start, destination, grid, nodeachter, index) + distance(nodeachter, destination)

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
    if (node[2]<10 and node[2]>=0 and node[1]<17 and node[1]>=0 and node[0]>=0 and node[0]<18):
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
    stop = 0
    for x in range(18):
        for y in range(17):
            for z in range (10):
                if grid[x][y][z] < minimum and grid[x][y][z]>100:
                    minimum = grid[x][y][z]
                    xvalue = x
                    yvalue = y
                    zvalue = z

    if minimum == 10000:
        stop = 1

    coordinates = [xvalue, yvalue , zvalue]
    return coordinates, stop

# route wordt geplaatst, alle nodes zijn gegeven
def findroute(gridwithnodes, locfrom, locto, start, direction):
    print('in findroute')
    index = 0
    route = []
    route.append(locto)
    route.append(start)
    count = 0
    while distance(locfrom, start) != 1:
        count += 1
        if count == 1000:
            sys.exit()
        routeelement = checkclosednode(direction, start)
        print(routeelement)
        route.append(routeelement)
        start = routeelement
    return route


def Gcost(start, destination, grid, node, index):
    if index ==1:
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
    

    elif index ==2:
        if node in surround_list:
            count_surrounded = surround_list.count(node)
            if grid[start[0]][start[1]][start[2]] > 10000:
                gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1 + 10*count_surrounded + 14 - 2*node[2]
            else:
                gcost = 1 + 10*count_surrounded + 14 - 2*node[2]
            return gcost
        else:
            if grid[start[0]][start[1]][start[2]] > 10000:
                gcost = grid[start[0]][start[1]][start[2]] - 10000 - distance(start, destination) + 1 + 14 - 2*node[2]
            else:
                gcost = 1 + 14 - 2*node[2]
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
    # if end location cant be reached, delete one of lines on surrounding gridpoints
    # check every surrounding gridpoint, delete most appropriate line
    for nextLocTo in netPoint.toSurround:
        for netPointToDelete in routeBookDone:
            for routePoint in netPointToDelete.route:
                if nextLocTo == [routePoint[0], routePoint[1], routePoint[2]]:
                    if grid[routePoint[0], routePoint[1], routePoint[2]] == 50 and \
                            netPointToDelete.locTo != [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]] and \
                            netPointToDelete.locFrom != [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]:
                        # remove line on grid
                        grid = delRoute(netPointToDelete.route, grid)
                        netPointToDelete.route = []

                        # append deleted line back to the routebookempty list
                        routeBookEmpty.append(netPointToDelete)
                        # delete line from routebookdone list
                        del routeBookDone[routeBookDone.index(netPointToDelete)]
                        # locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]

                        return routeBookEmpty, routeBookDone, grid, nextLocTo

def searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid):
    # check every surrounding gridpoint, delete most appropriate blocking line
    for nextLocFrom in netPoint.fromSurround:
        for netPointToDelete in routeBookDone:
            for routePoint in netPointToDelete.route:
                if nextLocFrom == [routePoint[0], routePoint[1], routePoint[2]]:
                    if grid[routePoint[0], routePoint[1], routePoint[2]] == 50 and \
                            netPointToDelete.locTo != [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]] and \
                            netPointToDelete.locFrom != [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]:
                        # remove line on grid
                        grid = delRoute(netPointToDelete.route, grid)
                        netPointToDelete.route = []

                        # append deleted line back to the routebookempty list
                        routeBookEmpty.append(netPointToDelete)
                        # delete line from routebookdone list
                        del routeBookDone[routeBookDone.index(netPointToDelete)]

                        return routeBookEmpty, routeBookDone, grid, nextLocFrom

def GcostForGates(gates):
    grid = np.zeros([18, 17, 10])
    for x in range(18):
        for y in range(17):
            for z in range(10):
                distancee = 0
                for i in gates:
                    distanceee = distance([x, y, z], [i.x, i.y, i.z])
                    distancee = distancee + distanceee
                grid[x][y][z] = 600 - distancee
    return grid


def replaceLines(routeBook, grid):
    for netPoint in routeBook:
        grid = delRoute(netPoint.route, grid)
        netPoint.route = Astar(netPoint, grid)
        grid = changeMat(netPoint.route, grid)
        print(netPoint.route)
    return routeBook, grid

def replaceLine(routeBook, grid, steps = 2000):
    for i in range(0, steps):
        print(i)
        index = random.randrange(0, len(routeBook))
        grid = delRoute(routeBook[index].route, grid)
        routeBook[index].route = Astar(routeBook[index], grid, 0)
        grid = changeMat(routeBook[index].route, grid)
        print(routeBook[index].route)
    return routeBook

def Astarroutemelle(routeBookAstar, grid, gates):
    # maak route met A-star
    # MOET IN FUNCTIE
    tic = time()
    print("beginbeginbegin")
    j = 0
    for netPoint in routeBookAstar:
        j = j + 1
        print(j)

        routee = Astar(netPoint, grid, 0)

        netPoint.route = routee
        grid = changeMat(routee, grid)
    toc = time()

    for route in routeBookAstar:
        print(route)

    plotLines(gates, routeBookAstar)
    print("time")
    print(toc - tic)
    score = getScore(routeBookAstar)
    print("score")
    print(score)
    quit()
