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
# Chips & Circuits main
############################################################

import sys
sys.path.insert(0, '../Data')


from numpy import genfromtxt
from copy import deepcopy
import functions
import options

# open de userinterface
response1, response2, netlist = options.userInterface()

# gebruik kleine of grote grid
if int(response2) < 4:
    size = "small"
    # laadt gates locaties voor kleine grid
    gatesLoc = genfromtxt('../Data/gates.csv', delimiter=';')
else:
    size = "large"
    # laadt gates locaties voor grote grid
    gatesLoc = genfromtxt('../Data/gates2.csv', delimiter=';')

# giet gate locaties in goede format
gates = functions.makeLocations(gatesLoc)

# maak grid met gates
grid = functions.gridMat(gates, size)

# # maak object van iedere netPoint in netlist
routeBook = functions.makeObjects(netlist, gates)
# # maak kopie van routeboek
routeBookEmpty = deepcopy(routeBook)

# bepaal lowerbound aka Manhattan distance van netlist
lowerBound, netlistDist = functions.manhattanDist(routeBook)
print("\nLowerbound score voor netlist", response2, ":", lowerBound)


# keuze 1: leg één van de 6 netlists
if response1 == '1':
    options.solveNetlist(routeBookEmpty, grid, size, gates)

# keuze 2: vergelijk verschillende invoernetlists
# (Dalton, Ui, beste uit random)
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
