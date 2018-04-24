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

from numpy import genfromtxt
from functions import *
import matplotlib.pyplot as plt
from netlists import *

# make appropriate format of gate locations
gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
gates = makeLocations(gatesLoc)

# show plot of gates in grid
# printPlot(gates)

# print grid in matrixform
grid = gridMat(gates)
print(grid)

# sort netlist by dalton-method
netlistDalton = daltonMethod(netlist_1, gates)

# connect gates
routeBook = []
totalscore = []
# for wire in netlistDalton:
wire = [0,4]
route1 = routeFinder(gates, wire)

# print(route1)
# changeMat(locfrom, grid)
# route.append(locfrom)

# plot grid, voor 3d watch https://www.youtube.com/watch?v=ZlpFQNVhB7I
plotMatrix(grid)

plotLines(gates)
