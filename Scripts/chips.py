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

# sort netlist by dalton-method
netlistDalton = daltonMethod(netlist_1, gates)

# make objects of netlist
routeBook = makeObjects(netlistDalton, gates)


# connect gates in netlist
routeBook = routeFinder(routeBook, grid)
totalScore = 0
for route in routeBook:
    # print(route)
    totalScore += len(route.route) - 1

# show needed output
# print(grid)
# print(totalScore)
plotLines(gates, routeBook)


# probeersel Melle
# print("hoi")
# print(grid)
# print("hoi")
# print(grid[1][10])




