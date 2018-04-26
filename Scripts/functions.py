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

def printPlot(gates):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Define ticks
    ticks = np.arange(0, 18, 1)
    ticks = np.arange(0, 18, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    for obj in gates:
        plt.plot(obj.x, obj.y, 'ro')    # WAAR KOMEN FIG EN PLOT SAMEN?
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

def routeFinder(gates, wire, grid):
    route = []
    locfrom = [gates[wire[0]].z, gates[wire[0]].y, gates[wire[0]].x]
    cursor = locfrom
    locto = [gates[wire[1]].z, gates[wire[1]].y, gates[wire[1]].x]
    # print(wire, locfrom, locto)
    # add begin point to route
    route.append([cursor[0], cursor[1], cursor[2]])
    # print(cursor)

    # look for best step until 1 step away from endpoint
    # HIER MOET EIGENLIJK NOG abs(locto[0] - cursor[0]) IN WHILE STATEMENT OM Z -AS TE CHECKEN
    # DIT WERKT NOG NIET, WORDT INFINITE LOOP, MOGELIJKE OPLOSSING ZIE ONDERAAN FUNCTIE MET RANDOMSTEP
    # MISSCHIEN OOK VOOR ALLE STAPJES EN ROUTE.APPEND IN LOSSE FUNCTIES
    while abs(locto[1] - cursor[1]) + abs(locto[2] - cursor[2]) > 1:

        # check if steps in y direction is bigger than x direction
        if abs(locto[1] - cursor[1]) > abs(locto[2] - cursor[2]):
            # step along y axis
            if locto[1] > cursor[1]:
                cursor[1] += 1
            else:
                cursor[1] -= 1
        else:
            # step along x axis
            if locto[2] > cursor[2]:
                cursor[2] += 1
            else:
                cursor[2] -= 1
        # save step in route
        route.append([cursor[0], cursor[1], cursor[2]])
        # print(cursor)

        # check if previous step is possible else delete and go up z-axis
        if grid[cursor[0], cursor[1], cursor[2]] != 99:
            # print([route[-1], "del"])
            del route[-1]
            # print(route[-1], "new cursor")
            cursor = [route[-1][0], route[-1][1], route[-1][2]]
            # print("up")
            cursor[0] += 1
            route.append([cursor[0], cursor[1], cursor[2]])
            # print(cursor)
        # if step down is possible, go down
        elif grid[cursor[0] - 1, cursor[1], cursor[2]] == 99.0 and cursor[0] > 0:
            # print("down")
            cursor[0] -= 1
            route.append([cursor[0], cursor[1], cursor[2]])
            # print(cursor)

        # make random step if stuck in infinite loop (does not work yet)
        # if len(route) >= 4 and route[-1] == route[-4]:
        #     randomstep = randint(1, 4)
        #     if randomstep == 1:
        #         cursor[1] += 1
        #     elif randomstep == 2:
        #         cursor[1] -= 1
        #     elif randomstep == 3:
        #         cursor[2] += 1
        #     else:
        #         cursor[2] -= 1
        #     route.append([cursor[0], cursor[1], cursor[2]])
        #     print("randomstep")

    # add end point to route
    route.append(locto)
    # print(locto)
    return route

def changeMat(route, grid):
    for step in route:
        grid[step[0], step[1], step[2]] = 50
    return grid

def plotMatrix(grid):
    plt.imshow(grid)
    plt.show()


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
    return(netlistversion3)



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


def plotLines (gates):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_xlim([0,18])
    ax.set_ylim([0,13])
    ax.set_zlim([0,7])
    ax.set_xticks(np.arange(0, 18, 1))
    ax.set_yticks(np.arange(0, 13, 1))
    ax.set_zticks(np.arange(0, 7, 1))
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')


    for gate in gates:
        ax.scatter(gate.x, gate.y, 0)

    plt.show()



# hier begint het Astar algoritme met bijbehorende functies
def Astar(grid, wire, gates):
    route = []
    locfrom = [gates[wire[0]].z, gates[wire[0]].y, gates[wire[0]].x]
    cursor = locfrom
    gridwithnodes = grid
    locto = [gates[wire[1]].z, gates[wire[1]].y, gates[wire[1]].x]
    return route

 def putnodes(start, grid, locfrom, destination):

     nodes = []
     nodelinks = [start[0], start[1], start[2]-1]

     if (grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] == 99):
         grid[nodelinks[0]][nodelinks[1]][nodelinks[2]] = 100 + distance(start, locfrom) + distance(start, destination)


         




 def distance(location, destination):
    z_dist = abs(destination[0] - location[0])
    y_dist = abs(destination[1] - location[1])
    x_dist = abs(destination[2] - location[2])
    distancee = z_dist + y_dist + x_dist
    return distancee

def checkexistance(node):
