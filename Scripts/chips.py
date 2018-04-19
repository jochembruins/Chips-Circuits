# python script
###########################################################
# chips.py
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
###########################################################
# instalrequirements:
# pip3 install numpy
# pip3 install matplotlib

from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

# make objects per gate
class Location(object):
    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" % (self.gate, self.x, self.y, self.z)

def main():
    # read gates data
    gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')
    
    gates = makeLocations(gatesloc)
    
    printPlot(gates)

    grid = gridMat(gates)
    
    print(grid)
    

    


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
    matgrid = np.zeros([13,18])
    for gate in gates:
        matgrid[gate.y,gate.x] = gate.gate
    return matgrid 

if __name__ == "__main__":
    main()
