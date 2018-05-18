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
from time import time

from numpy import genfromtxt
from functions import *
import matplotlib.pyplot as plt
from netlists import *
from classes import *
from surroundings_gates import *
from copy import deepcopy
from random import shuffle

## DATA
# make appropriate format of gate locations
gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
gates = makeLocations(gatesLoc)

# initialize 13 x 18 x 8 (= L x W x H) grid with gates
grid = gridMat(gates)

# maak netlist
netlistDalton = wire.daltonMethod(netlist_1, gates)[0]

# make object for each netlist item
routeBook = makeObjects(netlistDalton, gates)
for route in routeBook:
    print(route)

# maak kopie van routeboek
routeBookEmpty = deepcopy(routeBook)

# ## RANDOM ROUTEFINDER
# # leg wires van netlist adhv random netlist volgordes
# randomRoute = randomRouteBook(routeBookEmpty, gates, 1000)

# # # HILLCLIMBER
# # laat hilclimber werken
# HillClimber = hillClimb(randomRoute[0], randomRoute[1], gates, 1000)

# # krijg beste routeboek
# routeBookBest = HillClimber[0]

# # check route hillclimber
# check = checker(routeBookBest)

# print(HillClimber[1])

# # plot gates en lijnen
# plotLines(gates, routeBookBest)

## A-star

# routes die werken voor test
# dalton = [(2, 20), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13), (15, 17), (20, 10), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4
# ), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

dalton = [(20, 10), (3, 15), (15, 5), (3, 23), (5, 7), (15, 21), (13, 18), (1, 2), (3, 5), (10, 4), (7, 13), (3, 2), (22, 16), (22, 13), (15, 17), (22, 11), (11, 24), (6, 14), (16, 9), (19, 5), (15, 8), (10, 7), (23, 4
), (19, 2), (3, 4), (7, 9), (23, 8), (9, 13), (20, 19)]

routeBookAstar = makeObjects(dalton, gates)

# maak route met A-star
# MOET IN FUNCTIE
tic = time()
j=0
for route in routeBookAstar:
    j=j+1
    print(j)
    if j==21:
        break
    routee = Astar(gates, route.netPoint, grid)
    route.route = routee
    grid = changeMat(routee, grid)
toc = time()

for route in routeBookAstar:
    print(route)

plotLines(gates, routeBookAstar)
print(tic-toc)
score = getScore(routeBookAstar)
print(score)
quit()
tic = time()

for i in dalton:
    print(i)
    print(j)
    routeee = Astar(gates, i, grid)
    grid = changeMat(routeee, grid)
    j=j+1
    if j ==29:
        print("man man man")
        for x in range(18):
            for y in range(13):
                for z in range(8):
                    if grid[x][y][z] != 99:
                        print("x: ", end='')
                        print(x, end='')
                        print(" y: ", end='')
                        print(y, end='')
                        print(" z: ", end='')
                        print(z, end='')
                        print(" grid: ", end='')
                        print(grid[x][y][z])
        print("man man man")


toc = time()
print(toc-tic)
print("man man man")
for x in range(18):
    for y in range(13):
        for z in range(8):
            if grid[x][y][z] != 99:
                print("x: ", end='')
                print(x, end='')
                print(" y: ", end='')
                print(y, end='')
                print(" z: ", end='')
                print(z, end='')
                print(" grid: ", end='')
                print(grid[x][y][z])

print("man man man")

print("score")
score = 0
for x in range(18):
    for y in range(13):
        for z in range(8):
            if grid[x][y][z] == 50:
                score = score + 1

print(score)

