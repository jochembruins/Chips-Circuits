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
import sys
sys.path.insert(0, '../Data')

from time import time
from progressbar import ProgressBar
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import netlists
import classes
from copy import deepcopy
from random import shuffle
import statistics
import pandas as pd
import functions

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
    print("Gebruik: chips.py N \nN = 1, 2, 3, 4, 5, 6; "
          "waar '1' staat voor netlist 1")
    exit()

# gebruik kleine of grote grid
if commArg < 4:
    size = "small"
    # laadt gates locaties voor kleine grid
    gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
else:
    size = "large"
    # laadt gates locaties voor grote grid
    gatesLoc = genfromtxt('../Data/gates2.csv', delimiter=';')

## PREPAREER DATA
# giet gate locaties in goede format
gates = functions.makeLocations(gatesLoc)

# maak grid met gates
grid = functions.gridMat(gates, size)

# # maak object van iedere netPoint in netlist DIT MOET NAAR BENEDEN ZOMETEENEEE
routeBook = functions.makeObjects(netlist, gates)
# # maak kopie van routeboek
routeBookEmpty = deepcopy(routeBook)


# bepaal lowerbound aka Manhattan distance van netlist
# DIT MOET IN DE OUTPUTTABEL ERGENS NEERGEZET WORDEN
lowerBound, netlistDist = functions.manhattanDist(routeBook)
print("Lowerbound score voor netlist", commArg, ":", lowerBound)


# ## VERGELIJK VERSCHILLENDE NETLISTS ---------------------------------------
# # maak netlists met Ui/Dalton methode
# netlistDalton = classes.wire.daltonMethod(netlist, gates)
# netlistUi = classes.wire.uiMethod(netlist, gates)


# # sla ingaande routebook van beste oplossing randomroute op
# randomRouteBookIn = functions.randomRouteBook(routeBookEmpty, gates, size, 100)[0]
# randomRouteNetlistIn = []
# for object in randomRouteBookIn:
#     randomRouteNetlistIn.append(object.netPoint)

# netlistCompare = [netlistDalton, netlistUi, randomRouteNetlistIn]

# # bereid voortgangsbar voor
# pbar = ProgressBar()
# print("Hillclimber - replaceline algoritme")

# for netlist in pbar(netlistCompare):
#     tic = time()

#     # maar variabel aan
#     eindstandNetlist = []

#     # maak object van iedere netPoint, maak lijst van alle netPoints
#     routeBook = functions.makeObjects(netlist, gates)
#     routeBookEmpty = deepcopy(routeBook)

#     # leg routes met gewogen Astar algoritme
#     routesFound = functions.aStarRouteFinder(routeBookEmpty, grid, size)

#     # maak nieuw grid adhv het beste gevonden routebook
#     for route in routesFound[0]:
#         grid = functions.changeMat(route.route, grid)

#     # verbeter route door met pure A* lijnen opnieuw te leggen
#     routesBetter = functions.replaceLine(routesFound[0], grid, 0, size, 500)

#     if netlistCompare.index(netlist) == 0:
#         compare = routesBetter[1]
#     else:
#         compare = pd.concat([compare, routesBetter[1]], axis=1, join='inner')

#     # info ingaande routeBook
#     print("\nBeginstand netlist: ", netlist)
#     netlistDist = functions.manhattanDist(routeBook)[1]
#     print("Manhattan distance van netPoints: ", netlistDist)

#     for object in routesBetter[0]:
#         eindstandNetlist.append(object.netPoint)
#     # print info over resultaten
#     print("Eindstand netlist: ", eindstandNetlist)
#     print("Manhattan distance van netPoints: ", functions.manhattanDist(routesBetter[0])[1])

#     print("score voor netlist =", functions.getScore(routesBetter[0]))
#     # statistics.plotChip(gates, routesBetter[0], size)

#     # reset grid
#     grid = functions.gridMat(gates, size)

#     toc = time()
#     runtime = toc - tic
#     print("runtime:", runtime)

# compare.columns = ['Dalton', 'Ui', 'Random']
# statistics.plotLine(compare, 'Vergelijking sorteermethodes')


# ## RANDOM ROUTEFINDER --------------------------------------------------
# # leg wires van netlist adhv random netlist volgordes
# # met breakthrough algoritme
# # 4e argument = aantal verschillende netlists <<<< dit moet in docstring volgens mij
# randomRoute = functions.randomRouteBook(routeBookEmpty, gates, size, 100)
#
# # print info over uitkomst
# score = functions.getScore(randomRoute[2])
# print("Beste score van random:", score)
# check = functions.checker(randomRoute[2])
# statistics.plotChip(gates, randomRoute[2], size)
#
# zelfdemiss = functions.breakThroughFinder(randomRoute[0], grid)
# check = functions.checker(zelfdemiss[1])
# score = functions.getScore(zelfdemiss[1])
# print(score)


# Vergelijk HillClimbers A* --------------------------

randomRouteBook = functions.randomRouteBook(routeBookEmpty, gates, size, 100)
#maak nieuw grid adhv het beste gevonden routebook

# HILLCLIMBER: WISSEL TWEE NETPOINTS, LEG HELE NETLIST OPNIEUW ----------
# laat hilclimber werken
HillClimber = functions.hillClimb(randomRouteBook[2], randomRouteBook[1] , gates, size, 1000)

# sla data op om HillClimbers te vergelijken
compare = HillClimber[2]

# verkrijg kloppende grid
for route in randomRouteBook[2]:
    grid = functions.changeMat(route.route, grid)

# verbeter route door met pure A* lijnen opnieuw te leggen
# eerst in volgorde van de routeboek, daarna op willekeurige volgorde
for i in range(0, 2):
    # maak deepcopy zodat we de routeboek twee keer kunnen gebruiken
    routeBook = deepcopy(randomRouteBook[2])
    
    # verkrijg kloppende grid
    for route in randomRouteBook[2]:
        grid = functions.changeMat(route.route, grid)
    
    # verbeter met replaceLine
    NewRoute = functions.replaceLine(routeBook, grid, i, size, 1000)
    
    # voeg de data bij elkaar
    compare = pd.concat([compare, NewRoute[1]], axis=1, join='inner')

# verander namen columns
compare.columns = ['Hillclimber met Breakthrough', 'Replacelines op volgorde', 'Replacelines willekeurig']

# plot lijngrafiek
statistics.plotLine(compare, 'Hillclimber en Replacelines')

# # krijg beste routeboek
# routeBookBest = HillClimber[0]

# #check route hillclimber
# check = functions.checker(routeBookBest)

# print(HillClimber[1])

# # plot gates en lijnen
# statistics.plotChip(gates, routeBookBest, size)

## LEG MET Astar GEWOGEN EN VERBETER MET PURE
newRoutes = functions.aStarRouteFinder(routeBookEmpty, grid, size)
print(functions.checker(newRoutes[0]))
print(functions.getScore(newRoutes[0]))


# maak nieuw grid adhv het beste gevonden routebook
for route in newRoutes[0]:
    grid = functions.changeMat(route.route, grid)

# DIT MOET NOG AANGEPAST WORDEN OP NIEUWE INDEX IN FUNCTIE
# verbeter route door met pure A* lijnen opnieuw te leggen
NewRoute = functions.replaceLine(newRoutes[0],
                                 grid, 1,
                                 size, 1000)

# print info over uitkomsten
print(functions.getScore(NewRoute[0]))
print(functions.checker(NewRoute[0]))
print(len(NewRoute[0]))
statistics.plotChip(gates, NewRoute[0], size)

