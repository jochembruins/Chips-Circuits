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
import options



print("\n\nCHIPS & CIRCUITS\n"
          "Welkom bij de programmeertheoriecase van de Veganboyz\n"
          "(aka Melle Gelok, Jochem Bruins, Noah van Grinsven)\n")
print("Wat zou je willen zien?\n"
      "1: Los één van de 6 netlists op\n"
      "2: Het effect van de volgorde van een netlists\n"
      "3: De output van 'Breaktrough algoritme'\n"
      "4: De output van 'Gewogen Astar' algoritme\n"
      "5: Vergelijking van 3 verschillende hillclimbers")
while(True):
    response1 = input("Maak een keuze: ")
    if str.isnumeric(response1) is False or int(response1) < 1 or int(response1) > 5:
        print("Dit is geen geldige input\n"
                "Voorbeeld van geldige input is: 1, 2, 3, 4 of 5")
    else:
        break

if response1 == '1':
    print("Kies uit netlist 1 - 6")

    while (True):
        response2 = input("Maak een keuze: ")
        if str.isnumeric(response2) is False or int(response2) > 6 or int(
            response1) < 1:
            print("Dit is geen geldige input\n"
                  "Voorbeeld van geldige input is: 1, 2, 3, 4, 5 of 6")
        else:
            break

    if response2 == '1':
        netlist = netlists.netlist_1
    elif response2 == '2':
        netlist = netlists.netlist_2
    elif response2 == '3':
        netlist = netlists.netlist_3
    elif response2 == '4':
        netlist = netlists.netlist_4
    elif response2 == '5':
        netlist = netlists.netlist_5
    else:
        netlist = netlists.netlist_6

else:
    print("Kies uit netlist 1 - 3")
    while(True):
        response2 = input("Maak een keuze: ")
        if str.isnumeric(response2) is False or int(response2) > 3 or int(
            response2) < 1:
            print("Dit is geen geldige input\n"
                  "Voorbeeld van geldige input is: 1, 2 of 3")
        else:
            break

    if response2 == '1':
        netlist = netlists.netlist_1
    elif response2 == '2':
        netlist = netlists.netlist_2
    else:
        netlist = netlists.netlist_3

# gebruik kleine of grote grid
if int(response2) < 4:
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
lowerBound, netlistDist = functions.manhattanDist(routeBook)
print("\nLowerbound score voor netlist", response2, ":", lowerBound)



# keuze 1: leg één van de 6 netlists
if response1 == '1':
    options.solveNetlist(routeBookEmpty, grid, size, gates)

# keuze 2: vergelijk verschillende invoernetlists (Dalton, Ui, beste uit random)
if response1 == '2':
    options.compareNetlists(netlist, gates, routeBookEmpty, size, response2, grid)

# keuze 3: zoek de beste geldige routes met het breaktrough algoritme
if response1 == '3':
        options.breakThrough(routeBookEmpty, gates, size, response2)

# keuze 4: zoek de beste geldige routes het gewogen Astar algoritme
if response1 == '4':
    options.weightedAStar(routeBookEmpty, gates, grid, size)

# keuze 5: vergelijk 3 verschillende hillclimbers
if response1 == '5':
    options.compareHillClimbers(routeBookEmpty, gates, size, response2, grid)
