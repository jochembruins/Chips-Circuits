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
############################################################

from time import time

from numpy import genfromtxt
import functions
import matplotlib.pyplot as plt
import netlists
import classes
from copy import deepcopy
from random import shuffle
import statistics
import pandas as pd

## DATA
# make appropriate format of gate locations
gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
gates = functions.makeLocations(gatesLoc)

# initialize 13 x 18 x 8 (= L x W x H) grid with gates
grid = functions.gridMat(gates)

# maak netlist
netlistDalton = classes.wire.daltonMethod(netlists.netlist_1, gates)[0]

# make object for each netlist item
routeBook = functions.makeObjects(netlistDalton, gates)

# maak kopie van routeboek
routeBookEmpty = deepcopy(routeBook)



# RANDOM ROUTEFINDER
# leg wires van netlist adhv random netlist volgordes
randomRoute = functions.randomRouteBook(routeBookEmpty, gates, 100)
score = functions.getScore(randomRoute[2])
# statistics.plotChip(gates, randomRoute[2])


for route in randomRoute[2]:
	grid = functions.changeMat(route.route, grid)



NewRoute = functions.replaceLine(randomRoute[2], grid, 1, 100)
replaceData = NewRoute[1]
print(replaceData)


# # HILLCLIMBER
# laat hilclimber werken
HillClimber = functions.hillClimb(randomRoute[0], randomRoute[1], gates, 100)
hillData = HillClimber[2]
print(hillData)

result = pd.concat([replaceData, hillData], axis=1, join='inner')
print(result)
statistics.plotLine(result, 'Hillclimber en Replacelines')

# krijg beste routeboek
routeBookBest = HillClimber[0]

#check route hillclimber
check = functions.checker(routeBookBest)

print(HillClimber[1])

# plot gates en lijnen
statistics.plotChip(gates, routeBookBest)

## A-star

# newRoutes = functions.astarRouteFinder(routeBookEmpty, grid)

# print(len(newRoutes))

# print(functions.checker(newRoutes))

# print(functions.getScore(newRoutes))

# for route in newRoutes:
# 	print(route)

# statistics.plotChip(gates, newRoutes)

# NIET VERWIJDEREN
# routes die werken voor test
# dalton = [(2, 20), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13), (15, 17), (20, 10), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4
# ), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]


# dalton = [(20, 10), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13), (15, 17), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4
# ), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

# routeBookAstar = functions.makeObjects(dalton, gates)
# routeBookAstar = functions.Astarroutemelle(routeBookAstar, grid, gates)
# quit()


# routeBookAstar = functions.makeObjects(netlists.netlist_1, gates)

# routeBookAstar = astarRouteFinder(routeBookAstar, grid)

# routeBookAstar = functions.astarRouteFinder(routeBookAstar, grid)


# print(len(routeBookAstar[1]))
# print(len(routeBookAstar[0]))
# for ding in routeBookAstar[1]:
#     print(ding)

# plotLines(gates, routeBookAstar[1])

# maak route met A-star
# MOET IN FUNCTIE
# tic = time()
# j=0
# for route in routeBookAstarEmpty:
#     j=j+1
#     print(j)
#     if j==21:
#         break
#     routee = functions.Astar(gates, route.netPoint, grid)
#     route.route = routee
#     grid = functions.changeMat(routee, grid)
# toc = time()

# for route in routeBookAstar:
#     print(route)

# statistics.plotChip(gates, routeBookAstar)
# print(tic-toc)
# score = functions.getScore(routeBookAstar)
# print(score)
# quit()
# tic = time()

# for i in dalton:
#     print(i)
#     print(j)
#     routeee = functions.Astar(gates, i, grid)
#     grid = functions.changeMat(routeee, grid)
#     j=j+1
#     if j ==29:
#         print("man man man")
#         for x in range(18):
#             for y in range(13):
#                 for z in range(8):
#                     if grid[x][y][z] != 99:
#                         print("x: ", end='')
#                         print(x, end='')
#                         print(" y: ", end='')
#                         print(y, end='')
#                         print(" z: ", end='')
#                         print(z, end='')
#                         print(" grid: ", end='')
#                         print(grid[x][y][z])
#         print("man man man")


# toc = time()
# print(toc-tic)
# print("man man man")
# for x in range(18):
#     for y in range(13):
#         for z in range(8):
#             if grid[x][y][z] != 99:
#                 print("x: ", end='')
#                 print(x, end='')
#                 print(" y: ", end='')
#                 print(y, end='')
#                 print(" z: ", end='')
#                 print(z, end='')
#                 print(" grid: ", end='')
#                 print(grid[x][y][z])

# print("man man man")

# print("score")
# score = 0
# for x in range(18):
#     for y in range(13):
#         for z in range(8):
#             if grid[x][y][z] == 50:
#                 score = score + 1

# print(score)
