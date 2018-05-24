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
import pandas as pd
import statistics

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

def gridMat(gates, chip = "groot"):
    if chip == "groot":
        # make matrix of grid
        matGrid = np.zeros([18, 17, 10]) + 99

        for gate in gates:
            matGrid[gate.x, gate.y, gate.z] = gate.gate
        return matGrid

    else:
        # make matrix of grid
        matGrid = np.zeros([18, 13, 10]) + 99

        for gate in gates:
            matGrid[gate.x, gate.y, gate.z] = gate.gate
        return matGrid

def getLowerBound(routeBook):
    lowerBound = 0
    for netPoint in routeBook:
        x_dist = abs(netPoint.locFrom[0] - netPoint.locTo[0])
        y_dist = abs(netPoint.locFrom[1] - netPoint.locTo[1])
        z_dist = abs(netPoint.locFrom[2] - netPoint.locTo[2])
        lowerBound += z_dist + y_dist + x_dist
    return lowerBound

def randomRouteBook(routeBook, gates, steps=1000):

    random.seed(2)
    bestRouteBookIn = []

    score = 2000
    file  = open('../csv/random.csv', "w")
    writer = csv.writer(file, delimiter=',')

    randomData = pd.DataFrame(columns=['I','Score'])

    for i in range(0, steps):
        print(i)
        newRouteBook = routeBook
        shuffle(newRouteBook)

        grid = gridMat(gates)

        tmp_newRouteBook = deepcopy(newRouteBook)

        # checkt of het route vinden is gelukt
        finished = False

        newScore = score

        # probeer nieuwe route te vinden
        try:
            newRouteFound = breakThroughFinder(tmp_newRouteBook, grid)[1]
            finished = True
        except:
            finished = False

        # bereken nieuwe score
        if finished:
            newScore = getScore(newRouteFound)
            print("oude score random: ", score)
            print("nieuwe score random: ", newScore)
            writer.writerow([i, newScore])
            # newRow = pd.DataFrame({'I': i, 'Score': newScore}, ignore_index=True)
            randomData = randomData.append({'I': i, 'Score': newScore}, ignore_index=True)
            check = checker(newRouteFound)

            if check == True:
                # sla score en route op als beste is
                if newScore < score:
                    bestRouteBookIn = deepcopy(newRouteBook)
                    bestRouteFound = deepcopy(newRouteFound)
                    score = newScore
                    print('betere oplossing')
                else:
                    print('slechtere oplossing')
            else:
                for ding in newRouteFound:
                    print(ding)

    statistics.plotRandom(randomData)
    file.close()
    return bestRouteBookIn, score, bestRouteFound, grid


def breakThroughFinder(routeBook, grid):
    routeBookEmpty = routeBook
    routeBookDone = []
    count = 0
    while routeBookEmpty != []:
        for netPoint in routeBookEmpty:
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

            if count == 300:
                # print('meer dan 150')
                sys.exit

            for step in route:
                if step[2] > 15:
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
    hillData = pd.DataFrame(columns=['Score Hillclimber'])

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
            newRouteFound = breakThroughFinder(tmp_newRouteBook, grid)[1]
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
        hillData = hillData.append({'Score Hillclimber': score}, ignore_index=True)
    print(hillData)
    statistics.plotLine(hillData, 'Hillclimber')
    file.close()
    return bestRouteFound, score, hillData

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
def matrix_store_direction(chip):
    # richtingen matrix geven
    # 1 links
    # 2 rechts
    # 3 boven
    # 4 beneden
    # 5 voor
    # 6 achter

    if chip == "groot":
        matgrid = np.zeros([18, 17, 10])
        return matgrid
    else:
        matgrid = np.zeros([18, 13, 10])
        return matgrid

def aStarRouteFinder (routeBook, grid):
    """ Functie zoekt naar valide oplossing met gewogen Astar """
    
    # maak benodige variabelen aan
    tic = time()
    
    # lege grid
    gridEmpty = deepcopy(grid)
    
    # lijst met routes die nog gelegd moeten worden
    routeBookEmpty = deepcopy(routeBook)
    
    # nog lege lijst te vullen met gelegde routes
    routeBookDone = []
    
    # lijst om geslaagde netlist op te slaan
    routeBookSolved = deepcopy(routeBook)
    
    # counter voor het aantal iteraties
    loops = 0

    # loop totdat de routeboek leeg is
    while routeBookEmpty != []:
        # loop over alle elementen in de routeboek
        for netPoint in routeBookEmpty:
    
            # houd aantal loops bij
            loops += 1

            # controleert of de begingate van de lijn is ingesloten
            count = 0
            for loc in netPoint.fromSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            
            # verwijdert onnodige lijnen indien ingesloten
            if count == 5:
                routeBookEmpty, routeBookDone, grid = searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid)[0:3]   

            # controleert of de begingate van de lijn is ingesloten
            count = 0
            for loc in netPoint.toSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            
            # verwijdert onnodige lijnen indien ingesloten
            if count == 5:
                routeBookEmpty, routeBookDone, grid = searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid)[0:3]         

            # leg de route met Astar
            route = Astar(netPoint, grid, 2, 'groot')

            # voeg nieuwe route toe aan netPoins als Astar succesvol is
            if route != []:
                netPoint.route = route
                
                # update grid
                grid = changeMat(route, grid)

                # verplaats van 'emtpy-' naar 'done-' lijst
                doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
                routeBookDone.append(doneWire)
            
            # begin opnieuw als maximaal aantal loops is bereikt
            if loops == 150:
                lengthEmpty = len(routeBookEmpty)
                print(lengthEmpty)
                routeBookEmpty = routeBookEmpty + routeBookDone
                routeBookDone = []
                loops = 0
                
                # alleen shuffelen als de er meer dan vier routes onopgelost bleven
                if lengthEmpty > 4:
                    print('shuffle')
                    shuffle(routeBookEmpty)
                    
                # update laatste routeBook 
                print('update')
                routeBookSolved = deepcopy(routeBookEmpty)

                # maak grid weer leeg
                grid = deepcopy(gridEmpty)
                
    # bereken tijd
    toc = time()
    print(toc-tic)
    
    # check validiteit
    print(checker(routeBookDone))
    
    # krijg score
    print(getScore(routeBookDone))
    
    return routeBookDone, routeBookSolved


# Astar heeft een grid, gates en een wire nodig
def Astar(netPoint, grid, index, chip):
    locfrom = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
    gridwithnodes = deepcopy(grid)
    locto = [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]

    route=[]
    if distance(locfrom, locto) == 1:
        route.append(locto)
        route.append(locfrom)
    else:
        route = putwire(gridwithnodes, locfrom, locto, index, chip)
        if route != []:
            route.append(locfrom)
    route = list(reversed(route))
    return route

# putwire plaatst nodes totdat de locatie bereikt is
def putwire(gridwithnodes, locfrom, locto, index, chip):
    start = locfrom
    direction = matrix_store_direction(chip)
    stop = 0
    queue = []

    i=0

    while (distance(start, locto) != 1) and stop == 0:
        gridwithnodes, direction, queue = putnodes(start, gridwithnodes, locto, locfrom, direction, index, queue, chip)

        start, stop, queue = minimumnodes(gridwithnodes, queue)

        if i == 10000:
            quit()
        i = i + 1

    if stop == 0:
        route = findroute(gridwithnodes, locfrom, locto, start, direction)
    else:

        route=[]
    return route

#  nodes plaatsen
def putnodes(start, grid, destination, locfrom, direction, index, priority_queue, chip):

    if grid[start[0]][start[1]][start[2]] >= 100:

        # een  gesloten node is groter dan 10000
        grid[start[0]][start[1]][start[2]] = 10000 - 100 + grid[start[0]][start[1]][start[2]]

    nodelinks = [start[0]-1, start[1], start[2]]
    noderechts = [start[0]+1, start[1], start[2]]
    nodeboven = [start[0], start[1], start[2]+1]
    nodebeneden = [start[0], start[1], start[2]-1]
    nodevoor = [start[0], start[1] + 1, start[2]]
    nodeachter = [start[0], start[1] - 1, start[2]]



    if priority_queue != []:
        priority_queue.pop(0)

    nodelinkspotentieel = 1000000
    noderechtspotentieel = 1000000
    nodevoorpotentieel = 1000000
    nodeachterpotentieel = 1000000
    nodebovenpotentieel = 1000000
    nodebenedenpotentieel = 1000000

    # boven
    if checkexistance(nodeboven, chip) and check_isempty(nodeboven, grid):
        nodebovenpotentieel = 100 + Gcost(start, destination, grid, nodeboven, index) + distance(nodeboven, destination)

    if checkexistance(nodeboven, chip) and nodebovenpotentieel < grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]:
        former_value = grid[nodeboven[0]][nodeboven[1]][nodeboven[2]]
        grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
        direction[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 3
        index = priority_queue.index([former_value, [nodeboven[0], nodeboven[1], nodeboven[2]]])
        priority_queue.pop(index)
        priority_queue.append([nodebovenpotentieel, [nodeboven[0], nodeboven[1], nodeboven[2]]])

    elif checkexistance(nodeboven, chip) and grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] == 99:
        grid[nodeboven[0]][nodeboven[1]][nodeboven[2]] = nodebovenpotentieel
        direction[nodeboven[0]][nodeboven[1]][nodeboven[2]] = 3
        priority_queue.append([nodebovenpotentieel,[nodeboven[0], nodeboven[1], nodeboven[2]]])

    # beneden
    if checkexistance(nodebeneden, chip) and check_isempty(nodebeneden, grid):
        nodebenedenpotentieel = 100 + Gcost(start, destination, grid, nodebeneden, index) + distance(nodebeneden, destination)

    if checkexistance(nodebeneden, chip) and nodebenedenpotentieel < grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]:
        former_value = grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]]
        grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
        direction[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 4
        index = priority_queue.index([former_value, [nodebeneden[0], nodebeneden[1], nodebeneden[2]]])
        priority_queue.pop(index)
        priority_queue.append([nodebenedenpotentieel, [nodebeneden[0], nodebeneden[1], nodebeneden[2]]])

    elif checkexistance(nodebeneden, chip) and grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] == 99:
        grid[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = nodebenedenpotentieel
        direction[nodebeneden[0]][nodebeneden[1]][nodebeneden[2]] = 4
        priority_queue.append([nodebenedenpotentieel, [nodebeneden[0], nodebeneden[1], nodebeneden[2]]])



    # links
    if  checkexistance(nodelinks, chip) and check_isempty(nodelinks, grid):
        nodelinkspotentieel = 100 + Gcost(start, destination, grid, nodelinks, index) + distance(nodelinks, destination)


    if checkexistance(nodelinks, chip) and nodelinkspotentieel < grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]:
        former_value = grid[nodelinks[0]][nodelinks[1]][nodelinks[2]]
        grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
        direction[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 1
        index = priority_queue.index([former_value, [nodelinks[0], nodelinks[1], nodelinks[2]]])
        priority_queue.pop(index)
        priority_queue.append([nodelinkspotentieel, [nodelinks[0], nodelinks[1], nodelinks[2]]])

    elif checkexistance(nodelinks, chip) and grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99:
        grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = nodelinkspotentieel
        direction[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 1
        priority_queue.append([nodelinkspotentieel, [nodelinks[0], nodelinks[1], nodelinks[2]]])

    # rechts
    if checkexistance(noderechts, chip) and check_isempty(noderechts, grid):
        noderechtspotentieel = 100 + Gcost(start, destination, grid, noderechts, index) + distance(noderechts, destination)

    if checkexistance(noderechts, chip) and noderechtspotentieel < grid[noderechts[0]][noderechts[1]][noderechts[2]]:
        former_value = grid[noderechts[0]][noderechts[1]][noderechts[2]]
        grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
        direction[noderechts[0]][noderechts[1]][noderechts[2]] = 2
        index = priority_queue.index([former_value, [noderechts[0], noderechts[1], noderechts[2]]])
        priority_queue.pop(index)
        priority_queue.append([noderechtspotentieel, [noderechts[0], noderechts[1], noderechts[2]]])

    elif checkexistance(noderechts, chip) and grid[noderechts[0]][noderechts[1]][noderechts[2]] == 99:
        grid[noderechts[0]][noderechts[1]][noderechts[2]] = noderechtspotentieel
        direction[noderechts[0]][noderechts[1]][noderechts[2]] = 2
        priority_queue.append([noderechtspotentieel, [noderechts[0], noderechts[1], noderechts[2]]])



    # voor
    if checkexistance(nodevoor, chip) and check_isempty(nodevoor, grid):
        nodevoorpotentieel = 100 + Gcost(start, destination, grid, nodevoor, index) + distance(nodevoor, destination)

    if checkexistance(nodevoor, chip) and nodevoorpotentieel < grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]:
        former_value = grid[nodevoor[0]][nodevoor[1]][nodevoor[2]]
        grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
        direction[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 5
        index = priority_queue.index([former_value, [nodevoor[0], nodevoor[1], nodevoor[2]]])
        priority_queue.pop(index)
        priority_queue.append([nodevoorpotentieel, [nodevoor[0], nodevoor[1], nodevoor[2]]])

    elif checkexistance(nodevoor, chip) and grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] == 99:
        grid[nodevoor[0]][nodevoor[1]][nodevoor[2]] = nodevoorpotentieel
        direction[nodevoor[0]][nodevoor[1]][nodevoor[2]] = 5
        priority_queue.append([nodevoorpotentieel, [nodevoor[0], nodevoor[1], nodevoor[2]]])

    # achter
    if checkexistance(nodeachter, chip) and check_isempty(nodeachter, grid):
        nodeachterpotentieel = 100 + Gcost(start, destination, grid, nodeachter, index) + distance(nodeachter, destination)
    #     print("gcost")
    #     print(Gcost(start, destination, grid, nodeachter, index))

    if checkexistance(nodeachter, chip) and nodeachterpotentieel < grid[nodeachter[0]][nodeachter[1]][nodeachter[2]]:
        former_value = grid[nodeachter[0]][nodeachter[1]][nodeachter[2]]
        grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = nodeachterpotentieel
        direction[nodeachter[0]][nodeachter[1]][nodeachter[2]] = 6
        index = priority_queue.index([former_value, [nodeachter[0], nodeachter[1], nodeachter[2]]])
        priority_queue.pop(index)
        priority_queue.append([nodeachterpotentieel, [nodeachter[0], nodeachter[1], nodeachter[2]]])

    elif checkexistance(nodeachter, chip) and grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] == 99:
        grid[nodeachter[0]][nodeachter[1]][nodeachter[2]] = nodeachterpotentieel
        direction[nodeachter[0]][nodeachter[1]][nodeachter[2]] = 6
        priority_queue.append([nodeachterpotentieel, [nodeachter[0], nodeachter[1], nodeachter[2]]])

    return grid, direction, priority_queue


# distance berekenen tussen twee punten
def distance(location, destination):
    x_dist = abs(destination[0] - location[0])
    y_dist = abs(destination[1] - location[1])
    z_dist = abs(destination[2] - location[2])
    distancee = z_dist + y_dist + x_dist
    return distancee

# kijken of de te plaatsen node zich wel in het veld bevindt
def checkexistance(node, chip):
    if chip == "klein":
        if (node[0]>=0 and node[0]<18 and node[1]<13 and node[1]>=0 and node[2]<8 and node[2]>=0):
            return True
        else:
            return False

    if chip == "groot":
        if (node[0]>=0 and node[0]<18 and node[1]<17 and node[1]>=0 and node[2]<8 and node[2]>=0):
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
    if grid[node[0]][node[1]][node[2]] >= 10000:
        return False
    else:
        return True

# node met laagste f cost is het nieuwe startpunt waaruit nodes geplaatst worden
def minimumnodes(grid, queue):
    stop = 0
    coordinates = [0,0,0]
    if queue == []:
        stop =1
    else:
        queue.sort(key=lambda x: x[0])
        # index = queue.index([143, [11, 1, 0]])
        # print(index)

        if queue[0][0] <10000:
            xvalue = queue[0][1][0]
            yvalue = queue[0][1][1]
            zvalue = queue[0][1][2]
            coordinates = [xvalue, yvalue, zvalue]
        else:
            stop = 1
    return coordinates, stop, queue

# route wordt geplaatst, alle nodes zijn gegeven
def findroute(gridwithnodes, locfrom, locto, start, direction):
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
        route.append(routeelement)
        start = routeelement
    return route


def Gcost(start, destination, grid, node, index):
    # komt niet in de buurt van surrounded nodes
    if index == 1:
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

    # gaat de hoogte in en komt niet in de buurt van surrounded nodes
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

    # pure A*
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
    grid = np.zeros([18, 13, 10])
    for x in range(18):
        for y in range(13):
            for z in range(10):
                distancee = 0
                for i in gates:
                    distanceee = distance([x, y, z], [i.x, i.y, i.z])
                    distancee = distancee + distanceee
                grid[x][y][z] = 600 - distancee
    return grid

def replaceLine(routeBook, grid, order, steps = 2000):
    random.seed(2)
    replaceData = pd.DataFrame(columns=['Score ReplaceLine'])
    score = getScore(routeBook)
    bestRouteBook = routeBook
    bestGrid = grid

    for i in range(0, steps):
        newRouteBook = bestRouteBook
        newGrid = bestGrid

        if order == 1:
            index = random.randrange(0, len(newRouteBook))
            print(index)
        else:
            index = i % len(newRouteBook)
            print(index)
        
        print(newRouteBook[index].route)
        delRoute(newRouteBook[index].route, newGrid)
        newRouteBook[index].route = Astar(newRouteBook[index], newGrid, 0)
        print(newRouteBook[index].route)
        changeMat(newRouteBook[index].route, newGrid)
        print(checker(newRouteBook))
        newScore = getScore(newRouteBook)
        print(newScore)
        if newScore < score:
            bestGrid = newGrid
            score = newScore
            bestRouteBook = newRouteBook
        replaceData = replaceData.append({'Score ReplaceLine': score}, ignore_index=True)    
    print(replaceData)
    return bestRouteBook, replaceData

def Astarroutemelle(routeBookAstar, grid, gates):
    # maak route met A-star
    # MOET IN FUNCTIE
    tic = time()
    print("beginbeginbegin")
    j = 0
    for netPoint in routeBookAstar:
        j = j + 1

        print(j)

        routee = Astar(netPoint, grid, 2, "klein")

        netPoint.route = routee
        grid = changeMat(routee, grid)
    toc = time()

    print("time")
    print(toc - tic)
    score = getScore(routeBookAstar)
    print("score")
    print(getScore(routeBookAstar))
    for route in routeBookAstar:
        print(route)

    plotLines(gates, routeBookAstar)
    quit()

def Astarroutemelle2(routeBookAstar, grid, gates):
    # maak route met A-star
    # MOET IN FUNCTIE
    tic = time()
    print("beginbeginbegin")
    j = 0
    for netPoint in routeBookAstar:
        j = j + 1

        print(j)

        routee = Astar(netPoint, grid, 2, "groot")

        netPoint.route = routee
        grid = changeMat(routee, grid)
    toc = time()

    print("time")
    print(toc - tic)
    score = getScore(routeBookAstar)
    print("score")
    print(getScore(routeBookAstar))
    for route in routeBookAstar:
        print(route)


    statistics.plotChip(gates, routeBookAstar)

    plotLines(gates, routeBookAstar)
    quit()

def Astar_firstmap_firstnetlist(grid, gates):
    netlist = [(2, 20), (20, 10), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 0),
              (22, 16), (22, 13), (15, 17), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4),
              (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

    # dalton = [(2, 20), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13), (15, 17), (20, 10), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4
    # ), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

    routeBookAstar = makeObjects(netlist, gates)
    tic = time()
    print("beginbeginbegin")
    j = 0
    for netPoint in routeBookAstar:
        j = j + 1
        print(j)

        routee = Astar(netPoint, grid, 2)

        netPoint.route = routee
        grid = changeMat(routee, grid)
    toc = time()

    print("aantal netlist elementen")
    i = 0
    for j in routeBookAstar:
        if j.route != []:
            i = i + 1
        else:
            print("fout")
    print(i)

    quit()
    routeBookAstar = replaceLines(routeBookAstar, grid)[0]
    routeBookAstar = replaceLines(routeBookAstar, grid)[0]
    routeBookAstar = replaceLines(routeBookAstar, grid)[0]
    for route in routeBookAstar:

        print(route)

    print("time")
    print(toc - tic)
    score = getScore(routeBookAstar)
    print("score")
    print(score)
    print(checker(routeBookAstar))
    print("yes!!!")
    print(len(routeBookAstar))

    print("aantal netlist elementen")
    i = 0
    for j in routeBookAstar:
        if j.route != []:
            i = i + 1
        else:
            print("fout")
    print(i)

    plotLines(gates, routeBookAstar)
    quit()
