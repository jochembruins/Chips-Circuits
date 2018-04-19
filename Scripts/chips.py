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


gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')

gates = makeLocations(gatesloc)

# show plot of gates in grid
#printPlot(gates)

# print grid in matrix
grid = gridMat(gates)
#print(grid)

route(gates,grid)
# print(grid)
