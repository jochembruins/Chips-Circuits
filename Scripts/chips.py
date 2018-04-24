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

# connect gates in netlist
routeBook = []
totalscore = 0
for wire in netlistDalton:
    route = routeFinder(gates, wire)
    routeBook.append(route)
    totalscore += len(route) - 1
print(totalscore)
print(routeBook)


# changeMat(locfrom, grid)
# route.append(locfrom)

# plot grid, voor 3d watch https://www.youtube.com/watch?v=ZlpFQNVhB7I
plotMatrix(grid)


print("hoi")
print(grid)
print("hoi")
print(grid[1][10])