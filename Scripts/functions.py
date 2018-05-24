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
# Bevat alle functies die worden gebruikt in chips.py
###########################################################
from time import time
import progressbar
import csv
import numpy as np
import classes
import random
from random import shuffle
from copy import deepcopy
from surroundings_gates import surroundList
import pandas as pd
import statistics

np.set_printoptions(threshold=np.nan)
np.set_printoptions(linewidth=180)


def makeLocations(data):
    """ Giet locaties van gates uit file in objecten met x, y, z waarden"""
    gates = []
    for line in data:
        line = classes.Location(line[0],
                                int(line[1]),
                                int(line[2]),
                                int(line[3]))
        gates.append(line)
    return gates


def makeObjects(netlist, gates):
    """" Zet nodige info in de netPoint objecten"""
    emptyRouteBook = []

    for netPoint in netlist:
        locFrom = [gates[netPoint[0]].x,
                   gates[netPoint[0]].y,
                   gates[netPoint[0]].z]

        locTo = [gates[netPoint[1]].x,
                 gates[netPoint[1]].y,
                 gates[netPoint[1]].z]
        # omliggende punten van begin/eindpunt
        fromSurround = [[gates[netPoint[0]].x,
                         gates[netPoint[0]].y + 1,
                         gates[netPoint[0]].z],
                      [gates[netPoint[0]].x,
                       gates[netPoint[0]].y - 1,
                       gates[netPoint[0]].z],
                      [gates[netPoint[0]].x + 1,
                       gates[netPoint[0]].y,
                       gates[netPoint[0]].z],
                      [gates[netPoint[0]].x - 1,
                       gates[netPoint[0]].y,
                       gates[netPoint[0]].z ],
                      [gates[netPoint[0]].x,
                       gates[netPoint[0]].y,
                       gates[netPoint[0]].z + 1]]
        toSurround = [[gates[netPoint[1]].x,
                       gates[netPoint[1]].y + 1,
                       gates[netPoint[1]].z],
                      [gates[netPoint[1]].x,
                       gates[netPoint[1]].y - 1,
                       gates[netPoint[1]].z],
                      [gates[netPoint[1]].x + 1,
                       gates[netPoint[1]].y,
                       gates[netPoint[1]].z],
                      [gates[netPoint[1]].x - 1,
                       gates[netPoint[1]].y,
                       gates[netPoint[1]].z],
                      [gates[netPoint[1]].x,
                       gates[netPoint[1]].y,
                       gates[netPoint[1]].z +1]]
        route = []
        emptyRoute = classes.wire(netPoint, locFrom,
                                  locTo, fromSurround,
                                  toSurround, route)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def gridMat(gates, chip = "small"):
    """" Maakt matrix van de grid met gateslocatie-info"""
    if chip == "big":
        matGrid = np.zeros([18, 17, 30]) + 99
        for gate in gates:
            matGrid[gate.x, gate.y, gate.z] = gate.gate
        return matGrid

    else:
        matGrid = np.zeros([18, 13, 30]) + 99
        for gate in gates:
            matGrid[gate.x, gate.y, gate.z] = gate.gate
        return matGrid


def getLowerBound(routeBook):
    """ Bereken de lowerbound (manhattan distance) van gekozen netlist"""
    lowerBound = 0
    for netPoint in routeBook:
        x_dist = abs(netPoint.locFrom[0] - netPoint.locTo[0])
        y_dist = abs(netPoint.locFrom[1] - netPoint.locTo[1])
        z_dist = abs(netPoint.locFrom[2] - netPoint.locTo[2])
        lowerBound += z_dist + y_dist + x_dist
    return lowerBound


def randomRouteBook(routeBook, gates, steps=1000):
    """ Probeert willekeurige volgordes van de netlist met het breaktrough
    algoritme op te lossen, onthoudt de beste uitkomst """

    # zet seed voor shufflefunctie
    random.seed(2)

    # maak nodige variabelen aan
    bestRouteBookIn = []
    score = 2000

    # maak pandas bestand aan voor score-opslag
    randomData = pd.DataFrame(columns=['I', 'Score'])

    # loop voor aantal iteraties willekeurig algoritme
    for i in range(0, steps):

        # sla beginstand routebook op en shuffle
        newRouteBook = routeBook
        shuffle(newRouteBook)

        # maak nieuw lege grid aan
        grid = gridMat(gates)

        # maak nieuwe routebook aan waarin gewerkt kan worden
        tmp_newRouteBook = deepcopy(newRouteBook)

        finished = False
        # probeer nieuwe route te vinden met breaktrough algoritme
        try:
            newRouteFound = breakThroughFinder(tmp_newRouteBook, grid)[1]
            finished = True
        except:
            finished = False

        # bereken nieuwe score als resultaat gevonden is
        if finished:
            newScore = getScore(newRouteFound)

            randomData = randomData.append({'I': i, 'Score': newScore},
                                           ignore_index=True)
            check = checker(newRouteFound)

            if check is True:
                # sla score en route op als betere oplossing is gevonden
                if newScore < score:
                    bestRouteBookIn = deepcopy(newRouteBook)
                    bestRouteFound = deepcopy(newRouteFound)
                    score = newScore
    # plot histogram van randomscores
    statistics.plotRandom(randomData)
    return bestRouteBookIn, score, bestRouteFound, grid


def breakThroughFinder(routeBook, grid):
    """ algoritme om lijnen in netlist te leggen """

    # maak nodige variabelen aan
    routeBookEmpty = routeBook
    routeBookDone = []
    count = 0

    # run algoritme totdat alle lijnen gelegd zijn
    while routeBookEmpty != []:
        for netPoint in routeBookEmpty:

            # maak nodige variabelen aan
            route = []
            cursor = [netPoint.locFrom[0],
                      netPoint.locFrom[1],
                      netPoint.locFrom[2]]
            locTo = [netPoint.locTo[0],
                     netPoint.locTo[1],
                     netPoint.locTo[2]]

            # voeg beginpunt toe aan route
            route.append([cursor[0], cursor[1], cursor[2]])

            # als begin en eindpunt niet naast elkaar zitten,
            # bepaal eerste en laatste stap
            if stepsDifference(locTo, cursor) != 1:
                # zoek vrij punt om eindpunt heen
                for nextLocTo in netPoint.toSurround:
                    if grid[nextLocTo[0], nextLocTo[1], nextLocTo[2]] == 99:
                        locTo = [nextLocTo[0], nextLocTo[1], nextLocTo[2]]
                        break

                # als eindpunt niet bereikt kan worden,
                # verwijder geschikte omliggende lijn
                if locTo == [netPoint.locTo[0],
                             netPoint.locTo[1],
                             netPoint.locTo[2]]:
                    routeBookEmpty, routeBookDone, grid, locTo \
                        = searchLocTo(netPoint, routeBookEmpty,
                                      routeBookDone, grid)

                # make first step in available direction
                for nextLocFrom in netPoint.fromSurround:
                    if grid[nextLocFrom[0],
                            nextLocFrom[1],
                            nextLocFrom[2]] == 99:
                        cursor = [nextLocFrom[0],
                                  nextLocFrom[1],
                                  nextLocFrom[2]]
                        route.append([cursor[0], cursor[1], cursor[2]])
                        break

                # if there is no valid first step possible,
                # delete one of lines on surrounding gridpoints
                if cursor == [netPoint.locFrom[0],
                              netPoint.locFrom[1],
                              netPoint.locFrom[2]]:
                    routeBookEmpty, routeBookDone, grid, \
                    [cursor[0], cursor[1], cursor[2]] \
                        = searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid)
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


def astarRouteFinder (routeBook, grid):
    tic = time()
    gridEmpty = deepcopy(grid)
    routeBookAstarEmpty = deepcopy(routeBook)
    routeBookAstarDone = []
    loops = 0

    while routeBookAstarEmpty != []:
        print('hier')
        for netPoint in routeBookAstarEmpty:
            
            loops += 1

            count = 0
            for loc in netPoint.fromSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            if count == 5:
                routeBookAstarEmpty, routeBookAstarDone, grid \
                    = searchLocFrom(netPoint, routeBookAstarEmpty,
                                    routeBookAstarDone, grid)[0:3]

            count = 0
            for loc in netPoint.toSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            if count == 5:
                routeBookAstarEmpty, routeBookAstarDone, grid \
                    = searchLocTo(netPoint, routeBookAstarEmpty,
                                  routeBookAstarDone, grid)[0:3]


            print(len(routeBookAstarEmpty))
            print(len(routeBookAstarDone))

            route = aStar(netPoint, grid, 2, 'klein')

            if route != []:
                netPoint.route = route
                grid = changeMat(route, grid)

                doneWire = routeBookAstarEmpty.pop\
                    (routeBookAstarEmpty.index(netPoint))
                routeBookAstarDone.append(doneWire)
            
            if loops == 150:
                routeBookAstarEmpty = routeBookAstarEmpty + routeBookAstarDone
                routeBookAstarDone = []
                #shuffle(routeBookAstarEmpty)
                grid = deepcopy(gridEmpty)
                loops = 0
                
    toc = time()
    print(toc-tic)
    for route in routeBookSolved:
        print(route.netPoint)
    for route in routeBookAstarDone:
        print(route)
    print(checker(routeBookAstarDone))
    print(getScore(routeBookAstarDone))
    return routeBookAstarDone, routeBookSolved


# Astar returnt een route tussen twee gates ofwel een wire
def aStar(netPoint, grid, index, chip):

    # vertrekpunt
    locFrom = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
    gridWithNodes = deepcopy(grid)

    # eindpunt
    locTo = [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]

    route=[]
    if distance(locFrom, locTo) == 1:
        route.append(locTo)
        route.append(locFrom)
    else:
        route = putWire(gridWithNodes, locFrom, locTo, index, chip)
        if route != []:
            route.append(locFrom)

    # route op juiste manier returnen
    route = list(reversed(route))
    return route

# putwire plaatst nodes totdat de locatie bereikt is
def putWire(gridWithNodes, locFrom, locTo, index, chip):
    start = locFrom

    # slaat richting node op
    direction = matrixStoreDirection(chip)
    stop = 0
    queue = []

    # nodes plaatsen zolang beginnode niet grenst aan bestemming
    while (distance(start, locTo) != 1) and stop == 0:
        gridWithNodes, direction, queue \
            = \
            putNodes(start, gridWithNodes, locTo, direction, index, queue, chip)

        start, stop, queue = minimumNodes(queue)

    #  als stop ongelijk 0, lege route returnen
    if stop == 0:
        route = findRoute(locFrom, locTo, start, direction)
    else:

        route=[]

    return route

#  nodes plaatsen
def putNodes(start, grid, destination, direction, index, priorityQueue, chip):

    # een gesloten node heeft waarde 10000
    closedNodeValue = 10000

    # als er vanuit startpunt node geplaatst is:
    if grid[start[0]][start[1]][start[2]] >= 100:

        # node updaten naar gesloten node
        grid[start[0]][start[1]][start[2]] = closedNodeValue - 100 + \
                                             grid[start[0]][start[1]][start[2]]

    # list met omringenden van start
    nodeList = [[start[0] - 1, start[1], start[2]],
                [start[0] + 1, start[1], start[2]],
                [start[0], start[1], start[2] + 1],
                [start[0], start[1], start[2] - 1],
                [start[0], start[1] + 1, start[2]],
                [start[0], start[1] - 1, start[2]]]

    # startpunt uit priority queue halen
    if priorityQueue != []:
        priorityQueue.pop(0)

    # de potentiële nodes worden met een groot getal geïnitialiseerd
    nodePotentieel = [1000000, 1000000, 1000000, 1000000, 1000000, 1000000]

    #  itereren aantal omringenden startpunt
    for i in range (0,6):

        # als node in grid en leeg of niet gesloten
        if checkExistance(nodeList[i], chip) \
                and checkIsEmpty(nodeList[i], grid):
            # potentiële nodewaarde
            nodePotentieel[i] = \
                100 + gCost(start, destination, grid, nodeList[i], index) \
                + distance(nodeList[i], destination)

        # als node bestaat en potentiële waarde lager dan waarde
        if checkExistance(nodeList[i], chip) and nodePotentieel[i] < grid[
            nodeList[i][0]][nodeList[i][1]][nodeList[i][2]]:
            formerValue = grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]]
            grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] \
                = nodePotentieel[i]

            # richting updaten
            direction[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] = i + 1
            index = priorityQueue.index([formerValue, [nodeList[i][0],
                                                       nodeList[i][1],
                                                       nodeList[i][2]]])

            # oorspronkelijke waarde node uit priority queue
            priorityQueue.pop(index)

            # nieuwe waarde in priority queue
            priorityQueue.append([nodePotentieel[i], [nodeList[i][0],
                                                      nodeList[i][1],
                                                      nodeList[i][2]]])


        # node bestaat en potentiële waarde lager dan waarde en niks geplaatst:
        elif checkExistance(nodeList[i], chip) and \
                grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] == 99:
            grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]]\
                = nodePotentieel[i]
            direction[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] = i + 1
            priorityQueue.append([nodePotentieel[i],
                                  [nodeList[i][0], nodeList[i][1],
                                   nodeList[i][2]]])

    return grid, direction, priorityQueue

# matrix met richtingen van nodes
def matrixStoreDirection(chip):
    if chip == "groot":
        matgrid = np.zeros([18, 17, 10])
        return matgrid
    else:
        matgrid = np.zeros([18, 13, 10])
        return matgrid

# distance berekenen tussen twee punten: HEURISTIEK
def distance(location, destination):
    xDist = abs(destination[0] - location[0])
    yDist = abs(destination[1] - location[1])
    zDist = abs(destination[2] - location[2])
    distancee = zDist + yDist + xDist
    return distancee

# kijken of de te plaatsen node zich wel in het veld bevindt
def checkExistance(node, chip):
    if chip == "klein":
        if (node[0]>=0 and node[0]<18 and node[1]<13 and node[1]>=0 and
                node[2]<8 and node[2]>=0):
            return True
        else:
            return False

    if chip == "groot":
        if (node[0]>=0 and node[0]<18 and node[1]<17 and node[1]>=0  and
                node[2]<8 and node[2]>=0):
            return True
        else:
            return False

# er kan een node op gridelement geplaatst worden indien deze niet gesloten is:
def checkIsEmpty(node, grid):
    closedNodeValue = 10000
    emptyGridValue = 99
    if grid[node[0]][node[1]][node[2]] >= emptyGridValue and \
            grid[node[0]][node[1]][node[2]] < closedNodeValue:
        return True
    else:
        return False

# node met laagste f-cost is het nieuwe startpunt waaruit nodes geplaatst worden
def minimumNodes(queue):
    stop = 0
    coordinates = [0,0,0]

    # als de queue leeg is,  dan is elke veld bereikbaar gesloten
    if queue == []:
        # stop commando geven
        stop = 1
    else:
        # sorteer priority queue
        queue.sort(key=lambda x: x[0])

        # als eerste element niet gesloten node:
        if queue[0][0] <10000:
            xValue = queue[0][1][0]
            yValue = queue[0][1][1]
            zValue = queue[0][1][2]
            coordinates = [xValue, yValue, zValue]
        else:
            stop = 1
    return coordinates, stop, queue

# route wordt geplaatst, alle nodes zijn gegeven
def findRoute(locFrom, locTo, start, direction):
    route = []
    route.append(locTo)
    route.append(start)

    # zolang het vertrekpunt niet bereikt is
    while distance(locFrom, start) != 1:

        # kijk naar waar gesloten node wijst
        routeElement = checkClosedNode(direction, start)

        # zet element in de route
        route.append(routeElement)
        start = routeElement
    return route


def gCost(start, destination, grid, node, index):
    clodesNodeValue = 10000

    #  komt niet in de buurt van surrounded nodes
    if index == 1:

        # als de node naast een gate ligt
        if node in surroundList:

            # hoeveelheid gates die naast node liggen
            countSurrounded = surroundList.count(node)

            # als startpunt gesloten node
            if grid[start[0]][start[1]][start[2]] > clodesNodeValue:

                # gcost += 1  + 10 tot de macht hoeveelheid gates
                gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue - \
                        distance(start, destination) + 1 + 10**countSurrounded
            else:
                gCost = 1 + 10**countSurrounded
            return gCost
        else:
            if grid[start[0]][start[1]][start[2]] > clodesNodeValue:

                # gcost += 1
                gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue - \
                        distance(start, destination) + 1
            else:
                gCost = 1
            return gCost

    # gaat de hoogte in en komt niet in de buurt van surrounded nodes
    elif index == 2:
        maximumHeightGrid = 7

        if node in surroundList:
            countSurrounded = surroundList.count(node)
            if grid[start[0]][start[1]][start[2]] > clodesNodeValue:

                # gcost += 1  + 10 tot macht gates + 14 - 2*Z-dimensie node
                gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue - \
                        distance(start, destination) + 1 + 10*countSurrounded \
                        + 2*(maximumHeightGrid - node[2])
            else:
                gCost = 1 + 10*countSurrounded + 2*(maximumHeightGrid - node[2])
            return gCost
        else:
            if grid[start[0]][start[1]][start[2]] > clodesNodeValue:
                gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue - \
                        distance(start, destination) + 1 + \
                        2*(maximumHeightGrid - node[2])
            else:
                gCost = 1 + 2*(maximumHeightGrid - node[2])
            return gCost

    # pure A*
    else:
        if grid[start[0]][start[1]][start[2]] > clodesNodeValue:
            gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue \
                    - distance(start, destination) + 1
        else:
            gCost = 1
        return gCost

# kijk waar element vandaag wijst
def checkClosedNode(direction, start):
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


        if checkExistance(nodelinks):
            list.append(nodelinks)
        if checkExistance(noderechts):
            list.append(noderechts)
        if checkExistance(nodeboven):
            list.append(nodeboven)
        if checkExistance(nodebeneden):
            list.append(nodebeneden)
        if checkExistance(nodevoor):
            list.append(nodevoor)
        if checkExistance(nodeachter):
            list.append(nodeachter)
    list=sorted(list)
    return list

def searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid):
    # if end location cant be reached, delete one of lines
    # on surrounding gridpoints
    # check every surrounding gridpoint, delete most appropriate line
    for nextLocTo in netPoint.toSurround:
        for netPointToDelete in routeBookDone:
            for routePoint in netPointToDelete.route:
                if nextLocTo == [routePoint[0], routePoint[1], routePoint[2]]:
                    if grid[routePoint[0], routePoint[1], routePoint[2]] == 50 \
                            and netPointToDelete.locTo != [netPoint.locTo[0],
                                                       netPoint.locTo[1],
                                                       netPoint.locTo[2]] and \
                            netPointToDelete.locFrom != [netPoint.locTo[0],
                                                         netPoint.locTo[1],
                                                         netPoint.locTo[2]]:
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
                    if grid[routePoint[0], routePoint[1], routePoint[2]] == 50 \
                            and netPointToDelete.locTo != [netPoint.locFrom[0],
                                                       netPoint.locFrom[1],
                                                       netPoint.locFrom[2]] \
                            and netPointToDelete.locFrom != [
                                                        netPoint.locFrom[0],
                                                         netPoint.locFrom[1],
                                                         netPoint.locFrom[2]]:
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
        newRouteBook[index].route = aStar(newRouteBook[index], newGrid, 0)
        print(newRouteBook[index].route)
        changeMat(newRouteBook[index].route, newGrid)
        print(checker(newRouteBook))
        newScore = getScore(newRouteBook)
        print(newScore)
        if newScore < score:
            bestGrid = newGrid
            score = newScore
            bestRouteBook = newRouteBook
        replaceData = \
            replaceData.append({'Score ReplaceLine': score}, ignore_index=True)
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

        routee = aStar(netPoint, grid, 2, "klein")

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

        routee = aStar(netPoint, grid, 2, "groot")

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
    quit()

def Astar_firstmap_firstnetlist(grid, gates):
    netlist = [(2, 20), (20, 10), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21),
               (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 0),
              (22, 16), (22, 13), (15, 17), (22, 11), (11, 24), (6, 14),
               (16, 9), (19, 5), (15, 8), (10, 7), (23, 4),
              (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

    # dalton = [(2, 20), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18),
    # (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13),
    # (15, 17), (20, 10), (22, 11), (11, 24), (6, 14), (16, 9),
    # (19, 5), (15, 8), (10, 7), (23, 4
    # ), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

    routeBookAstar = makeObjects(netlist, gates)
    tic = time()
    print("beginbeginbegin")
    j = 0
    for netPoint in routeBookAstar:
        j = j + 1
        print(j)

        routee = aStar(netPoint, grid, 2)

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
