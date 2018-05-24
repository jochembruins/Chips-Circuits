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
                         gates[netPoint[0]].z],
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
                       gates[netPoint[1]].z + 1]]
        route = []
        emptyRoute = classes.wire(netPoint, locFrom,
                                  locTo, fromSurround,
                                  toSurround, route)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def gridMat(gates, chip):
    """" Maakt matrix van de grid met gateslocatie-info"""
    if chip == "large":
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


def randomRouteBook(routeBook, gates, chip, steps=1000):
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
        grid = gridMat(gates, chip)

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
    """ algoritme om lijnen in netlist te leggen
        heuristiek: weg belemmerd, ga omhoog!"""

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
                # verwijder geschikte omliggende lijn bij eindpunt
                if locTo == [netPoint.locTo[0],
                             netPoint.locTo[1],
                             netPoint.locTo[2]]:
                    routeBookEmpty, routeBookDone, grid, locTo \
                        = searchLocTo(netPoint, routeBookEmpty,
                                      routeBookDone, grid)

                # maak eerste stap in beschikbare richting
                for nextLocFrom in netPoint.fromSurround:
                    if grid[nextLocFrom[0],
                            nextLocFrom[1],
                            nextLocFrom[2]] == 99:
                        cursor = [nextLocFrom[0],
                                  nextLocFrom[1],
                                  nextLocFrom[2]]
                        route.append([cursor[0], cursor[1], cursor[2]])
                        break

                # als geen eerste stap mogelijk is,
                # verwijder geschikte omliggende lijn bij beginpunt
                if cursor == [netPoint.locFrom[0],
                              netPoint.locFrom[1],
                              netPoint.locFrom[2]]:
                    routeBookEmpty, routeBookDone, grid, \
                    [cursor[0], cursor[1], cursor[2]] \
                        = searchLocFrom(netPoint, routeBookEmpty,
                                        routeBookDone, grid)
                    route.append([cursor[0], cursor[1], cursor[2]])

            # zet stappen totdat 1 stap af van eindpunt
            while stepsDifference(locTo, cursor) > 1:

                # kijken of stapjes in y-richting groter is dan x-richting
                if abs(locTo[1] - cursor[1]) > abs(locTo[0] - cursor[0]):
                    # zet stap in y-richting
                    if locTo[1] > cursor[1]:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1
                else:
                    # zet stap in x-richting
                    if locTo[0] > cursor[0]:
                        cursor[0] += 1
                    else:
                        cursor[0] -= 1
                # save stapje in route
                route.append([cursor[0], cursor[1], cursor[2]])

                # check voor dubbele stappen
                if len(route) > 3 and route[-1] == route[-3]:
                    del route[-2:]
                if len(route) > 4 and route[-1] == route[-5]:
                    del route[-4:]

                # als stap niet mogelijk is verwijder stap en ga omhoog in z-as
                if grid[cursor[0], cursor[1], cursor[2]] != 99:
                    del route[-1]
                    cursor = [route[-1][0], route[-1][1], route[-1][2]]
                    cursor[2] += 1
                    route.append([cursor[0], cursor[1], cursor[2]])

                    # check voor dubbele stappen
                    if len(route) > 3 and route[-1] == route[-3]:
                        del route[-2:]

                    # als omhoog gaan niet mogelijk is, wire erboven verwijderen
                    if grid[cursor[0], cursor[1], cursor[2]] != 99:
                        for netPointToDelete in routeBookDone:
                            for routePoint in netPointToDelete.route:
                                if [cursor[0], cursor[1], cursor[2]] \
                                        == [routePoint[0],
                                            routePoint[1],
                                            routePoint[2]]:
                                    # verwijder lijn in grid
                                    grid = delRoute(netPointToDelete.route,
                                                    grid)
                                    netPointToDelete.route = []

                                    # voeg verwijderde lijn terug aan
                                    # routebookempty list
                                    routeBookEmpty.append(netPointToDelete)
                                    del routeBookDone[
                                        routeBookDone.index(netPointToDelete)]
                                    break

                # als een stap naar beneden mogelijk is doe dat
                elif grid[cursor[0], cursor[1], cursor[2] - 1] == 99.0 \
                        and cursor[2] > locTo[2]:
                    while grid[cursor[0], cursor[1], cursor[2] - 1] == 99.0 \
                            and cursor[2] > locTo[2]:
                        cursor[2] -= 1
                        route.append([cursor[0], cursor[1], cursor[2]])

                        # check voor dubbele stappen
                        if len(route) > 3 and route[-1] == route[-3]:
                            del route[-2:]

                # als boven eindpunt ga naar beneden en delete blokkerende
                # lijnen
                if [cursor[0], cursor[1]] == [locTo[0], locTo[1]] \
                        and cursor[2] != locTo[2]:

                    # vind lijnen onder de cursor
                    for netPointToDelete in routeBookDone:
                        for routePoint in netPointToDelete.route:
                            if [cursor[0], cursor[1], cursor[2] - 1] \
                                    == [routePoint[0],
                                        routePoint[1],
                                        routePoint[2]]:
                                # verwijder lijn in grid
                                grid = delRoute(netPointToDelete.route, grid)
                                netPointToDelete.route = []

                                # voeg verwijderde lijn terug in routebookempty
                                # list
                                routeBookEmpty.append(netPointToDelete)
                                del routeBookDone[
                                    routeBookDone.index(netPointToDelete)]
                                cursor[2] -= 1

                                route.append([cursor[0], cursor[1], cursor[2]])
                                break

                # verwijder eerste stappen die niet nuttig waren
                if len(route) > 2 \
                        and stepsDifference(netPoint.locFrom, cursor) == 1:
                    del route[1:len(route) - 1]

                # als 1 stap weg van eindbestemming stop
                if stepsDifference(netPoint.locTo, cursor) == 1:
                    break

            # voeg eindpunt aan route toe
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

            # delete netPoint van  empty list, voeg toe aan done list
            doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
            routeBookDone.append(doneWire)

            # update matrix for route
            changeMat(netPoint.route, grid)
    return routeBookEmpty, routeBookDone, grid


def changeMat(route, grid):
    """ verander waarden in matrix bij gelukte route"""
    for step in route[1:-1]:
        grid[step[0], step[1], step[2]] = 50
    return grid


def delRoute(route, grid):
    """ verander waarden in matrix als route verwijderd moet worden"""
    for step in route[1:-1]:
        grid[step[0], step[1], step[2]] = 99
    return grid


def stepsDifference(vector1, vector2):
    """ reken afstand tussen twee punten uit """
    difference = abs(vector1[0] - vector2[0]) + abs(vector1[1] - vector2[1]) \
                 + abs(vector1[2] - vector2[2])
    return difference


def getScore(routeBook):
    """ bereken score van routebook"""
    score = 0
    for route in routeBook:
        score += (len(route.route) - 1)
    return score


def hillClimb(routeBook, score, gates, chip, steps=1000):
    # maak variabele om beste route book op te slaan
    print('in Hillclimber')
    bestRouteBook = routeBook
    file = open('../csv/hill.csv', "w")
    writer = csv.writer(file, delimiter=',')
    hillData = pd.DataFrame(columns=['Score Hillclimber'])

    # loop voor het aantal stappen
    for i in range(0, steps):
        # maak lege grid
        grid = gridMat(gates, chip)

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

            if check is True:
                # sla score en route op als beste is
                if newScore <= score:
                    bestRouteBook = deepcopy(newRouteBook)
                    bestRouteFound = deepcopy(newRouteFound)
                    score = newScore
                    print('lager')
                else:
                    print('hoger')

        writer.writerow([i, score])
        hillData = hillData.append({'Score Hillclimber': score},
                                   ignore_index=True)
    print(hillData)
    statistics.plotLine(hillData, 'Hillclimber')
    file.close()
    return bestRouteFound, score, hillData


def checker(routeBook):
    """ Checkt voor duplicaten in gevonden oplossing"""
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


def aStarRouteFinder(routeBook, grid, size):
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
                routeBookEmpty, routeBookDone, grid \
                    = searchLocFrom(netPoint, routeBookEmpty,
                                    routeBookDone, grid)[0:3]

            # controleert of de begingate van de lijn is ingesloten
            count = 0
            for loc in netPoint.toSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1

            # verwijdert onnodige lijnen indien ingesloten
            if count == 5:
                routeBookEmpty, routeBookDone, grid, locTo \
                    = searchLocTo(netPoint, routeBookEmpty,
                                  routeBookDone, grid)

            # leg de route met Astar
            route = aStar(netPoint, grid, 2, size)

            # voeg nieuwe route toe aan netPoints als Astar succesvol is
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
                routeBookEmpty = routeBookEmpty + routeBookDone
                routeBookDone = []
                loops = 0

                # alleen shuffelen als de er meer dan vier
                # routes onopgelost bleven
                if lengthEmpty > 4:
                    shuffle(routeBookEmpty)

                # update laatste routeBook
                print('update')
                routeBookSolved = deepcopy(routeBookEmpty)

                # maak grid weer leeg
                grid = deepcopy(gridEmpty)

    # bereken tijd
    toc = time()
    print("Runningtime :", toc - tic)

    return routeBookDone, routeBookSolved


def aStar(netPoint, grid, index, chip):
    """ Returnt een route tussen twee gates ofwel een wire """

    # vertrekpunt
    locFrom = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
    gridWithNodes = deepcopy(grid)

    # eindpunt
    locTo = [netPoint.locTo[0], netPoint.locTo[1], netPoint.locTo[2]]

    route = []
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


def putWire(gridWithNodes, locFrom, locTo, index, chip):
    """ Plaatst nodes totdat de locatie bereikt is """

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

        route = []

    return route


def putNodes(start, grid, destination, direction, index, priorityQueue, chip):
    """ Nodes plaatsen """

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

    # de potentiële nodes worden met een large getal geïnitialiseerd
    nodePotentieel = [1000000, 1000000, 1000000, 1000000, 1000000, 1000000]

    #  itereren aantal omringenden startpunt
    for i in range(0, 6):

        # als node in grid en leeg of niet gesloten
        if checkExistance(nodeList[i], chip) \
                and checkIsEmpty(nodeList[i], grid):
            # potentiële nodewaarde
            nodePotentieel[i] = \
                100 + gCost(start, destination, grid, nodeList[i], index) \
                + distance(nodeList[i], destination)

        # als node bestaat en potentiële waarde lager dan waarde
        if checkExistance(nodeList[i], chip) and nodePotentieel[i] < \
                grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]]:
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
            grid[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] \
                = nodePotentieel[i]
            direction[nodeList[i][0]][nodeList[i][1]][nodeList[i][2]] = i + 1
            priorityQueue.append([nodePotentieel[i],
                                  [nodeList[i][0], nodeList[i][1],
                                   nodeList[i][2]]])

    return grid, direction, priorityQueue


def matrixStoreDirection(chip):
    """ matrix met richtingen van nodes """

    if chip == "large":
        matgrid = np.zeros([18, 17, 10])
        return matgrid
    else:
        matgrid = np.zeros([18, 13, 10])
        return matgrid


def distance(location, destination):
    """ distance berekenen tussen twee punten: HEURISTIEK """

    xDist = abs(destination[0] - location[0])
    yDist = abs(destination[1] - location[1])
    zDist = abs(destination[2] - location[2])
    distancee = zDist + yDist + xDist
    return distancee


def checkExistance(node, chip):
    """ kijken of de te plaatsen node zich wel in het veld bevindt """

    if chip == "small":
        if (node[0] >= 0 and node[0] < 18 and node[1] < 13 and node[1] >= 0 and
                node[2] < 8 and node[2] >= 0):
            return True
        else:
            return False

    if chip == "large":
        if (node[0] >= 0 and node[0] < 18 and node[1] < 17 and node[1] >= 0
                and node[2] < 8 and node[2] >= 0):
            return True
        else:
            return False


def checkIsEmpty(node, grid):
    """ er kan een node op gridelement geplaatst
        worden indien deze niet gesloten is: """

    closedNodeValue = 10000
    emptyGridValue = 99
    if grid[node[0]][node[1]][node[2]] >= emptyGridValue \
            and grid[node[0]][node[1]][node[2]] < closedNodeValue:
        return True
    else:
        return False


def minimumNodes(queue):
    """ node met laagste f-cost is het nieuwe startpunt
        waaruit nodes geplaatst worden """

    stop = 0
    coordinates = [0, 0, 0]

    # als de queue leeg is,  dan is elke veld bereikbaar gesloten
    if queue == []:
        # stop commando geven
        stop = 1
    else:
        # sorteer priority queue
        queue.sort(key=lambda x: x[0])

        # als eerste element niet gesloten node:
        if queue[0][0] < 10000:
            xValue = queue[0][1][0]
            yValue = queue[0][1][1]
            zValue = queue[0][1][2]
            coordinates = [xValue, yValue, zValue]
        else:
            stop = 1
    return coordinates, stop, queue


def findRoute(locFrom, locTo, start, direction):
    """ route wordt geplaatst, alle nodes zijn gegeven """

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
                        distance(start, destination) + 1 + 10 ** countSurrounded
            else:
                gCost = 1 + 10 ** countSurrounded
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
                        distance(start, destination) + 1 + 10 * countSurrounded \
                        + 2 * (maximumHeightGrid - node[2])
            else:
                gCost = 1 + 10 * countSurrounded + 2 * (
                            maximumHeightGrid - node[2])
            return gCost
        else:
            if grid[start[0]][start[1]][start[2]] > clodesNodeValue:
                gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue - \
                        distance(start, destination) + 1 + \
                        2 * (maximumHeightGrid - node[2])
            else:
                gCost = 1 + 2 * (maximumHeightGrid - node[2])
            return gCost

    # pure A*
    else:
        if grid[start[0]][start[1]][start[2]] > clodesNodeValue:
            gCost = grid[start[0]][start[1]][start[2]] - clodesNodeValue \
                    - distance(start, destination) + 1
        else:
            gCost = 1
        return gCost


def checkClosedNode(direction, start):
    """ kijk waar element vandaag wijst """

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
    list = []
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
    list = sorted(list)
    return list


def searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid):
    """ zoek in omliggende punten van eindpunt welke lijnen daar liggen,
        verwijder de lijn die daar niks heeft te zoeken """

    for nextLocTo in netPoint.toSurround:
        for netPointToDelete in routeBookDone:
            for routePoint in netPointToDelete.route:
                if nextLocTo == [routePoint[0], routePoint[1], routePoint[2]]:
                    if grid[routePoint[0], routePoint[1], routePoint[2]] == 50 \
                            and netPointToDelete.locTo != [netPoint.locTo[0],
                                                           netPoint.locTo[1],
                                                           netPoint.locTo[2]] \
                            and netPointToDelete.locFrom != [netPoint.locTo[0],
                                                             netPoint.locTo[1],
                                                             netPoint.locTo[2]]:
                        # verwijder lijn van de grid
                        grid = delRoute(netPointToDelete.route, grid)
                        netPointToDelete.route = []

                        # avoeg verwijderde lijn terug aan
                        # routebookempty list

                        routeBookEmpty.append(netPointToDelete)
                        # verwijder lijn vanuit routebookdone list
                        del routeBookDone[routeBookDone.index(netPointToDelete)]
                        return routeBookEmpty, routeBookDone, grid, nextLocTo


def searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid):
    """ zoek in omliggende punten van beginpunt welke lijnen daar liggen,
        verwijder de lijn die daar niks heeft te zoeken """

    # check alle omringende gridpoint, delete blokkerende lijn
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
                        # haal lijn van grid weg
                        grid = delRoute(netPointToDelete.route, grid)
                        netPointToDelete.route = []

                        # voeg lijn toe in routebookempty list
                        routeBookEmpty.append(netPointToDelete)
                        # delete lijn van routebookdone list
                        del routeBookDone[routeBookDone.index(netPointToDelete)]

                        return routeBookEmpty, routeBookDone, grid, nextLocFrom


def GcostForGates(gates):
    """ maakt voor element in grid een gcostwaarde afhankelijk
        van de afstand tot de gates"""
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


def replaceLine(routeBook, grid, order, chip, steps = 2000):
    """ Hillclimber algoritme,
        neemt een bestaande oplossing, verwijderd vervolgens achter elkaar
        1 en zet deze terug met pure Astar algoritme
        order index "1" neemt telkens een random lijn, bij andere waarden
        wordt de volgorde van de routebook aangehouden """

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
        else:
            index = i % len(newRouteBook)

        delRoute(newRouteBook[index].route, newGrid)
        newRouteBook[index].route = aStar(newRouteBook[index], newGrid, 0, chip)
        changeMat(newRouteBook[index].route, newGrid)
        newScore = getScore(newRouteBook)
        if newScore < score:
            bestGrid = newGrid
            score = newScore
            # print(score)
            bestRouteBook = newRouteBook
        replaceData = \
            replaceData.append({'Score ReplaceLine': score}, ignore_index=True)
    # print(replaceData)
    return bestRouteBook, replaceData
