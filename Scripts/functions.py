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
        route = []
        emptyRoute = wire(point, locFrom, locTo, route)
        # print(emptyRoute)
        emptyRouteBook.append(emptyRoute)

    return emptyRouteBook


def printPlot(gates):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Define ticks
    ticks = np.arange(0, 18, 1)
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
    matgrid = np.zeros([7, 13, 18]) + 99

    for gate in gates:
        matgrid[gate.z, gate.y, gate.x] = gate.gate
    return matgrid


def routeFinder(routeBook, grid):
    routeBookEmpty = routeBook
    routeBookDone = []
    while routeBookEmpty != []:
        for netPoint in routeBookEmpty:
            route = []
            deleted = []
            cursor = [netPoint.locFrom[0], netPoint.locFrom[1], netPoint.locFrom[2]]
            # add begin point to route
            route.append([cursor[0], cursor[1], cursor[2]])

            # look for best step until 1 step away from endpoint
            while abs(netPoint.locTo[0] - cursor[0]) + abs(netPoint.locTo[1] - cursor[1]) + \
                    abs(netPoint.locTo[2] - cursor[2]) > 1:

                # check if steps in y direction is bigger than x direction
                if abs(netPoint.locTo[1] - cursor[1]) > abs(netPoint.locTo[2] - cursor[2]):
                    # step along y axis
                    if netPoint.locTo[1] > cursor[1]:
                        cursor[1] += 1
                    else:
                        cursor[1] -= 1
                else:
                    # step along x axis
                    if netPoint.locTo[2] > cursor[2]:
                        cursor[2] += 1
                    else:
                        cursor[2] -= 1
                # save step in route
                route.append([cursor[0], cursor[1], cursor[2]])

                # check if previous step is possible else delete and go up z-axis
                if grid[cursor[0], cursor[1], cursor[2]] != 99:
                    deleted.append(route[-1])
                    del route[-1]
                    cursor = [route[-1][0], route[-1][1], route[-1][2]]
                    cursor[0] += 1
                    route.append([cursor[0], cursor[1], cursor[2]])
                # if step down is possible, go down
                # HIER WHILE LOOP VAN MAKEN??
                elif grid[cursor[0] - 1, cursor[1], cursor[2]] == 99.0 and cursor[0] > 0:
                    cursor[0] -= 1
                    route.append([cursor[0], cursor[1], cursor[2]])

                # HIERIN WORDEN EEN PAAR DINGEN NIET GOED VERWIJDERD, WEET NIET WAAROM
                if len(deleted) > 2 and deleted[-1] == deleted[-2]:
                    for netPointToDelete in routeBookDone:
                        for routepoint in netPointToDelete.route:
                            # probeer verwijderen met kleine lijst
                            if deleted[-1] == [routepoint[0], routepoint[1], routepoint[2]]:
                                grid = delRoute(netPointToDelete.route[1:-1], grid)
                                netPointToDelete.route = []
                                routeBookEmpty.append(netPointToDelete)
                                print("Dit is weg", routeBookDone.index(netPointToDelete))
                                del routeBookDone[routeBookDone.index(netPointToDelete)]
                    # Dit hieronder moet in de IF statement hierboven, nu wordt er gek genoeg 2x del route[-5:] gedaan.
                    # Probleem is dat er dan weer een inf loop ontstaat omdat de cursor boven de eindgate uitkomt maar niet omlaag kan.
                    # mogelijke oplossing: na elif hierboven nieuwe if statement met als dit gebeurt de lijn eronder weghalen
                    cursor[0] -= 1
                    del route[-5:]
                    route.append([deleted[-1][0], deleted[-1][1], deleted[-1][2]])

            # add end point to route
            route.append(netPoint.locTo)
            netPoint.route = route

            print(routeBookEmpty.index(netPoint))
            doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
            print(doneWire)
            routeBookDone.append(doneWire)

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

# deze functie ordent de netlist
# hierbij wordt er geordend op lengte van een netlistelementconnectie (blauwe lijn)
# als argument wordt een netlist genomen + de gates
def daltonMethod(netlist, gate):
    # tweede versie van netlist opgeslagen
    netlistversion2 = netlist
    # lege derde versie van te definiëren netlist opgeslagen
    netlistversion3 = []
    # lengte netlist berekend
    k = len(netlist)

    # itereren over lengte netlist
    for j in range(0, k):

        # het minimum worddt op een hoog getal gezet
        minimum = 1000
        # numbernetlist wordt 0
        numbernetlist = 0

        # itereren over lengte netlist min j
        for i in range(0, k - j):
            # de eerste factor van wire opslaan in listelement1
            listelement1 = netlistversion2[i][0]
            # de tweede factor van wire opslaan in listelement2
            listelement2 = netlistversion2[i][1]

            # verschil in x-waarden netconnecties opslaan in x_verschil
            x_verschil = abs(gate[listelement1].x - gate[listelement2].x)
            # verschil in y-waarden netconnecties opslaan in y_verschil
            y_verschil = abs(gate[listelement1].y - gate[listelement2].y)
            som = x_verschil + y_verschil

            # als de som van x_verschil en y_verschil kleiner dan minimum
            if (som < minimum):
                minimum = som
                numbernetlist = i

        # zet zojuist bepaalde netlistelement in netlistversion3
        netlistversion3.append(netlistversion2[numbernetlist])
        # haalde aangewezen element uit netlistversion2
        netlistversion2.pop(numbernetlist)

    # return nieuwe netlist
    return (netlistversion3)


# deze functie ordent de netlist
# hierbij wordt er geordend of een netlistelementconnectie (blauwe lijn) aan de buitenkant ligt
# als argument wordt een netlist genomen + de gates
def UIMethod_forprint1(netlist, gate):
    # tweede versie van netlist opgeslagen
    netlistversion2 = netlist
    # lege derde versie van te definiëren netlist opgeslagen
    netlistversion3 = []
    # lengte netlist berekend
    k = len(netlist)

    # de breedte van het eerste veld is 17 (tellend vanaf 0)
    breedte = 17
    # de hoogte van het eerste veld is 12 (tellend vanaf 0)
    hoogte = 12

    # helftbreedte en hoogte worden berekend om het bord te scheiden
    helftbreedte = breedte / 2
    helfthoogte = hoogte / 2

    # itereren over lengte netlist
    for j in range(0, k):
        # het minimum worddt op een hoog getal gezet
        minimum = 1000
        # numbernetlist wordt 0
        numbernetlist = 0

        # itereren over lengte netlist min j
        for i in range(0, k - j):
            # de eerste factor van wire opslaan in listelement1
            listelement1 = netlistversion2[i][0]
            # de tweede factor van wire opslaan in listelement2
            listelement2 = netlistversion2[i][1]

            # check of de x-waarde in de eerste helft valt
            if (gate[listelement1].x <= helftbreedte):
                x1waarde = gate[listelement1].x
            else:
                # anders wordt de waarde breedte minus x-element
                x1waarde = breedte - gate[listelement1].x

            if (gate[listelement1].y <= helfthoogte):
                y1waarde = gate[listelement1].y
            else:
                y1waarde = hoogte - gate[listelement1].y

            # de waarde van de eerste gate is het minimum van de x1- en y1waarde
            waarde1 = min(x1waarde, y1waarde)

            if (gate[listelement2].x <= helftbreedte):
                x2waarde = gate[listelement2].x
            else:
                x2waarde = breedte - gate[listelement2].x

            if (gate[listelement2].y <= helfthoogte):
                y2waarde = gate[listelement2].y
            else:
                y2waarde = hoogte - gate[listelement2].y

            # de waarde van de tweede gate is het minimum van de x2- en y2waarde
            waarde2 = min(x2waarde, y2waarde)

            som = waarde1 + waarde2

            # als de som kleiner is dan het minimum
            if (som < minimum):
                minimum = som
                numbernetlist = i

        # zet zojuist bepaalde netlistelement in netlistversion3
        netlistversion3.append(netlistversion2[numbernetlist])
        # haalde aangewezen element uit netlistversion2
        netlistversion2.pop(numbernetlist)
    # return nieuwe netlist
    return (netlistversion3)


def plotLines(gates, routeBook):
    # maak een nieuwe plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # definieer assen
    ax.set_xlim([0, 18])
    ax.set_ylim([0, 13])
    ax.set_zlim([0, 7])

    # zet ticks op de assem
    ax.set_xticks(np.arange(0, 18, 1))
    ax.set_yticks(np.arange(0, 13, 1))
    ax.set_zticks(np.arange(0, 7, 1))

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
#         return True
#     else:
#         return False
#
# # als een element in matrix gelijk is aan 99 dan wordt is daar geen wire node of gate
#
# def check_isempty(node, grid):
#     if grid[node[0]][node[1]][node[2]] >= 99 and grid[node[0]][node[1]][node[2]]<10000:
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
#
# # node met laagste f cost is het nieuwe startpunt waaruit nodes geplaatst worden
# def minimumnodes(grid):
#     minimum = 10000
#     xvalue = 0
#     yvalue = 0
#     zvalue = 0
#     for x in range(18):
#         for y in range(13):
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
#     return route
#
# # closednode met laagste f cost, grenzend aan bepaald punt wordt bepaald
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

# closednode met laagste f cost, grenzend aan bepaald punt wordt bepaald
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