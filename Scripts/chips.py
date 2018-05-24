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
import numpy as np
import functions
import matplotlib.pyplot as plt
import netlists
import classes
from copy import deepcopy
from random import shuffle
import statistics
import pandas as pd
import sys

if len(sys.argv) == 1:
    print("Gebruik: chips.py N \nN = 1, 2, 3, 4, 5, 6; waar '1' "
          "staat voor netlist 1")
    exit()

commArg = int(sys.argv[1])

if commArg == 1:
    netlist = netlists.netlist_1
elif commArg == 2:
    netlist = netlists.netlist_2
elif commArg == 3:
    netlist = netlists.netlist_3
elif commArg == 4:
    netlist = netlists.netlist_4
elif commArg == 5:
    netlist = netlists.netlist_5
elif commArg == 6:
    netlist = netlists.netlist_6
else:
    print("Gebruik niet correct")
    print("Gebruik: chips.py N \nN = 1, 2, 3, 4, 5, 6; waar '1' staat voor netlist 1")
    exit()

# gebruik kleine of grote grid
if commArg < 4:
    size = "small"
    # laadt gates voor kleine grid
    gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
else:
    size = "big"
    # laadt gates voor grote grid
    gatesLoc = genfromtxt('../Data/gates2.csv', delimiter=';')

## PREPAREER DATA
# giet gate locaties in goede format

gates = functions.makeLocations(gatesLoc)

# maak grid met gates
grid = functions.gridMat(gates, size)

print(np.shape(grid))

# maak object van iedere netPoint
routeBook = functions.makeObjects(netlist, gates)

# bepaal lowerbound aka Manhattan distance van netlist
# DIT MOET IN DE OUTPUTTABEL ERGENS NEERGEZET WORDEN
lowerBound = functions.getLowerBound(routeBook)

# maak kopie van routeboek
routeBookEmpty = deepcopy(routeBook)

# ## RANDOM ROUTEFINDER
# # leg wires van netlist adhv random netlist volgordes
# # met breakthrough algoritme
# # 3e argument = aantal verschillende netlists
# randomRoute = functions.randomRouteBook(routeBookEmpty, gates, 100)
#
# # print info over uitkomst
# score = functions.getScore(randomRoute[2])
# print("Beste score van random:", score)
# check = functions.checker(randomRoute[2])
# statistics.plotChip(gates, randomRoute[2])

## DALTON METHODE
# netlistDalton = classes.wire.daltonMethod(netlist, gates)
# # maak object van iedere netPoint
# daltonRouteBook = functions.makeObjects(netlistDalton, gates)
#
# HIER ASTAR GEWOGEN EN HILLCLIMBER OP DALTONLIST

## UI METHODE
# netlistUi = classes.wire.UIMethod_forprint1(netlist, gates)
# # maak object van iedere netPoint
# uiRouteBook = functions.makeObjects(netlistUi, gates)
#
# HIER ASTAR GEWOGEN EN HILLCLIMBER OP UILIST

## HILLCLIMBER: VERWIJDER ÉÉN LIJN, LEG TERUG MET A*
# maak nieuw grid adhv het beste gevonden routebook
# for route in randomRoute[2]:
#     grid = functions.changeMat(route.route, grid)

# DIT MOET NOG AANGEPAST WORDEN OP NIEUWE INDEX IN FUNCTIE
# verbeter route door met pure A* lijnen opnieuw te leggen
# NewRoute = functions.replaceLine(randomRoute[2], grid, 1, 1000)

# print info over uitkomsten
# print(functions.getScore(NewRoute[0]))
# print(functions.checker(NewRoute[0]))
# print(len(NewRoute))
# for route in NewRoute:
#     print(route.route)
# functions.plotLines(gates, NewRoute)

# returnt lijst met scores na iedere iteratie
# replaceData = NewRoute[1]
# print(replaceData)

## HILLCLIMBER: WISSEL TWEE NETPOINTS, LEG HELE NETLIST OPNIEUW
# # laat hilclimber werken
# HillClimber = functions.hillClimb(randomRoute[0], randomRoute[1], gates, 1000)
# hillData = HillClimber[2]
# print(hillData)

#
# # maak een plot van beide hillclimbers
# result = pd.concat([replaceData, hillData], axis=1, join='inner')
# print(result)
# statistics.plotLine(result, 'Hillclimber en Replacelines')

# # krijg beste routeboek
# routeBookBest = HillClimber[0]

# #check route hillclimber
# check = functions.checker(routeBookBest)

# print(HillClimber[1])

# # plot gates en lijnen
# statistics.plotChip(gates, routeBookBest)

# A-star
#
# newRoutes = functions.astarRouteFinder(routeBookEmpty, grid)
#
# print(len(newRoutes))
#
# print(functions.checker(newRoutes[0]))
#
# print(functions.getScore(newRoutes[0]))
#
# for route in newRoutes[1]:
# 	print(route)
#
# statistics.plotChip(gates, newRoutes[0])
