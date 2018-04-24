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
from classes import *

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
    matgrid = np.zeros([13,18]) + 99


    for gate in gates:
        matgrid[gate.y, gate.x] = gate.gate
    return matgrid

def routeFinder(gates, wire):
    route = []
    locfrom = [gates[wire[0]].y, gates[wire[0]].x]
    cursor = locfrom
    locto = [gates[wire[1]].y, gates[wire[1]].x]

    while abs(locto[0] - cursor[0]) + abs(locto[1] - cursor[1]) > 1:
        if abs(locto[0] - cursor[0]) > abs(locto[1] - cursor[1]):
            if locto[0] > cursor[0]:
                cursor[0] += 1
            else:
                cursor[0] -= 1
        else:
            if locto[1] > cursor[1]:
                cursor[1] += 1
            else:
                cursor[1] -= 1
        route.append(cursor)
        print(route)
    return route

def changeMat(newloc, grid):
    grid[newloc[0], newloc[1]] = 50
    return grid

def plotMatrix(grid):
    plt.imshow(grid)
    plt.show()

def daltonMethod(netlist, gate):
    netlistversion2 = netlist
    netlistversion3 = []
    k = len(netlist)

    for j in range(0, k):
        minimum = 1000
        numbernetlist = 0
        for i in range(0, k - j):
            listelement1 = netlistversion2[i][0]
            listelement2 = netlistversion2[i][1]
            x_verschil = abs(gate[listelement1].x - gate[listelement2].x)
            y_verschil = abs(gate[listelement1].y - gate[listelement2].y)
            som = x_verschil + y_verschil

            if (som < minimum):
                minimum = som
                numbernetlist = i

        netlistversion3.append(netlistversion2[numbernetlist])
        netlistversion2.pop(numbernetlist)

    return(netlistversion3)

def UIMethod_forprint1(netlist, gate):
    netlistversion2 = netlist
    netlistversion3 = []
    k = len(netlist)
    breedte = 17
    hoogte = 12
    helftbreedte = breedte / 2
    helfthoogte = hoogte / 2

    for j in range(0, k):
        minimum = 1000
        numbernetlist = 0
        for i in range(0, k - j):
            listelement1 = netlistversion2[i][0]
            listelement2 = netlistversion2[i][1]

            if (gate[listelement1].x <= helftbreedte):
                x1waarde = gate[listelement1].x
            else:
                x1waarde = breedte - gate[listelement1].x

            if (gate[listelement1].y <= helfthoogte):
                y1waarde = gate[listelement1].y
            else:
                y1waarde = hoogte - gate[listelement1].y



            if (gate[listelement2].x <= helftbreedte):
                x2waarde = gate[listelement2].x
            else:
                x2waarde = breedte - gate[listelement2].x

            if (gate[listelement2].y <= helfthoogte):
                y2waarde = gate[listelement2].y
            else:
                y2waarde = hoogte - gate[listelement2].y


            som = x1waarde + x2waarde + y1waarde +y2waarde

            if (som < minimum):
                minimum = som
                numbernetlist = i

        netlistversion3.append(netlistversion2[numbernetlist])
        netlistversion2.pop(numbernetlist)

    return(netlistversion3)