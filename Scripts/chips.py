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


gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')

gates = makeLocations(gatesloc)

# show plot of gates in grid
#printPlot(gates)

# print grid in matrix
grid = gridMat(gates)
#print(grid)

route(gates,grid)
# print(grid)


plotMatrix(grid)

netlist_1 = [(23, 4), (5, 7), (1, 2), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 2), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]

netlistdalton = daltonMethod(netlist_1, gates)