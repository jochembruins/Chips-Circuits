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
        matgrid[gate.y,gate.x] = gate.gate
    return matgrid

def route(gates,grid):
    locfrom = [gates[4].x, gates[4].y]
    locto = [gates[0].x, gates[0].y]

    # print(locfrom)
    while locfrom != locto:
        if abs(locto[0] - locfrom[0]) > abs(locto[1] - locfrom[1]):
            if locto[0] > locfrom[0]:
                locfrom[0] += 1
            else:
                locfrom[0] -= 1
            changeMat(locfrom,grid)
        else:
            if locto[1] > locfrom[1]:
                locfrom[1] += 1
            else:
                locfrom[1] -= 1
            changeMat(locfrom,grid)

        # print(locfrom)
    return grid
def changeMat(newloc, grid):
    print(grid)
    print("\n")
    grid[newloc] = 50

    return grid