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

grid = gridMat(gates)
gridAstar = gridMat2(gates)
print(gridAstar)


# netlistDalton = wire.daltonMethod(netlist_1, gates)
#
#
# routeBook = makeObjects(netlistDalton, gates)
#
# routeBookempty = deepcopy(routeBook)
#
# for route in routeBookempty:
#     print(route)

netlistDalton = wire.daltonMethod(netlist_1, gates)


routeBook = makeObjects(netlistDalton, gates)

routeBookempty = deepcopy(routeBook)

# AstarAll(routeBookempty, gridAstar)
for route in routeBookempty:
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


# show plot of gates in grid
# printPlot(gates)
# connect gates in netlist
#routeBook = routeFinder(routeBook, grid)[1]
#score = getScore(routeBook)
# print(score)
# score = 1000

# # laat hilclimber werken
# HillClimber = hillClimb(routeBookempty, score, gates, 5000)

# routeBookBest = HillClimber[0]
# for route in routeBookBest:
#     print(route.route)


# print(HillClimber[1])


# lol = checker(routeBookBest)
# print(lol)

# show needed output
# print(grid)
# print(totalScore)

# print grid in matrixform
# grid = gridMat(gates)
# emptyGrid = deepcopy(grid)
#
# # sort netlist by dalton-method


# netlistDalton = wire.daltonMethod(netlist_1, gates)
# print(netlistDalton)
#
#
# # # make objects of netlist

#
#
# # connect gates in netlist
# routeBook = routeFinder(routeBook, grid)[1]
# score = getScore(routeBook)
# # print(score)
#
#
# # laat hilclimber werken
# HillClimber = hillClimb(routeBookempty, score, gates, 1000)
#
# routeBookBest = HillClimber[0]
# for route in routeBookBest:
# 	print(route)
#
# print(HillClimber[1])
#
#
#
# # for route in routeBook:
# #     print(route)
#     # print(grid, "vol")
#
#
# # show needed output
# # print(grid)
# # print(totalScore)
# plotLines(gates, routeBookBest)
#
#
# # probeersel Melle
# # print("hoi")
# # print(grid)
# # print("hoi")
# # print(grid[1][10])
#
# # print(gates)
# # hoi = Astar(gates, (42, 3), grid)
# # print(hoi)
#
# netlistDalton = daltonMethod(netlist_1, gates)
# # print(netlistDalton)
# # make objects of netlist
# # routeBook = makeObjects(netlistDalton, gates)
#
#
# # connect gates in netlist
# # done = 2
# # while done != 0:
# #     for wire in routeBook:
# #         if wire.route == []:
# #             done = 1
# #         else:
# #             done = 0
# # grid = gridMat(gates)
#     # print(grid, "leeg")

# netlistDalton = daltonMethod(netlist_1, gates)
# print(netlistDalton)

# make objects of netlist
# routeBook = makeObjects(netlistDalton, gates)


# connect gates in netlist
# done = 2
# while done != 0:
#     for wire in routeBook:
#         if wire.route == []:
#             done = 1
#         else:
#             done = 0
# grid = gridMat(gates)
    # print(grid, "leeg")

