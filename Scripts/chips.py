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
from classes import *
from copy import deepcopy

# make appropriate format of gate locations
gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
gates = makeLocations(gatesLoc)

# show plot of gates in grid
# printPlot(gates)

# print grid in matrixform
grid = gridMat(gates)
emptyGrid = deepcopy(grid)

# sort netlist by dalton-method
netlistDalton = wire.daltonMethod(netlist_1, gates)


# # make objects of netlist
routeBook = makeObjects(netlistDalton, gates)

routeBookempty = deepcopy(routeBook)


# connect gates in netlist
routeBook = routeFinder(routeBook, grid)[1]

score = getScore(routeBook)
# print(score)


# laat hilclimber werken
HillClimber = hillClimb(routeBookempty, score, gates, 1000)

routeBookBest = HillClimber[0]
for route in routeBookBest:
	print(route)

print(HillClimber[1])



# for route in routeBook:
#     print(route)
    # print(grid, "vol")


# show needed output
# print(grid)
# print(totalScore)
plotLines(gates, routeBookBest)


# probeersel Melle
# print("hoi")
# print(grid)
# print("hoi")
# print(grid[1][10])
# print(gates)
# hoi = Astar(gates, (42, 3), grid)
# print(hoi)