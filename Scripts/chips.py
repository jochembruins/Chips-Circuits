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

## DATA
# make appropriate format of gate locations
gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
gates = makeLocations(gatesLoc)

# initialize 13 x 18 x 8 (= L x W x H) grid with gates
grid = gridMat(gates)

# make appropriate netlist order
netlistDalton = wire.daltonMethod(netlist_1, gates)

# make object for each netlist item
routeBook = makeObjects(netlistDalton, gates)

routeBookEmpty = deepcopy(routeBook)


## RANDOM ROUTEFINDER
# leg wires van netlist
# routeBookRandom = routeFinder(routeBook, grid)[1]
# score = getScore(routeBookRandom)
# print(score)

## A-star ALGORITM
# AstarAll(routeBookempty, gridAstar)

gridAstar = gridMat2(gates)
print(gridAstar)

for route in routeBookEmpty:
    print(route)

hoi = [(23, 4), (1, 2), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 2), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]

j=0
for i in hoi:
    print(j)
    routeee = Astar(gates, i, gridAstar)
    gridAstar = changeMat(routeee, gridAstar)
    j=j+1
    if j ==16:
        print("man man man")
        for x in range(18):
            for y in range(13):
                for z in range(8):
                    if gridAstar[x][y][z] != 99:
                        print("x: ", end='')
                        print(x, end='')
                        print(" y: ", end='')
                        print(y, end='')
                        print(" z: ", end='')
                        print(z, end='')
                        print(" grid: ", end='')
                        print(gridAstar[x][y][z])
        print("man man man")



## HILLCLIMBER
# score = 1000
# # laat hilclimber werken
# HillClimber = hillClimb(routeBookempty, score, gates, 5000)

# routeBookBest = HillClimber[0]
# for route in routeBookBest:
#     print(route.route)

# checkt juistheid van uitkomst hillclimber
# check = checker(routeBookBest)

# print beste score gevonden door hillclimber
# print(HillClimber[1])

# print score en laat plot zien
# print(check)
# plotLines(gates, routeBookBest)

