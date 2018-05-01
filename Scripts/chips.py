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
# print(grid)

# sort netlist by dalton-method
netlistDalton = daltonMethod(netlist_1, gates)

routeBook = []
totalscore = 0
# connect gates in netlist
for wire in netlistDalton:

    route = routeFinder(gates, wire, grid, routeBook)

    # save route and total score
    routeBook.append(route)
    totalscore += len(route) - 1

    # change matrix for steps in route
    changeMat(route[1:-1], grid)

    # print route per wire
    print(route)

# show needed output
# print(grid)
# print(routeBook)
# print(totalscore)


# uitprobeersel Melle
plotLines(gates, routeBook)
# print("hoi")
# print(grid)
# print("hoi")
# print(grid[1][10])




