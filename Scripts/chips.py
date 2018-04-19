# python script
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
from functions.py import *

def main():
    # read gates data
    gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')
    
    gates = makeLocations(gatesloc)
    
    printPlot(gates)

    grid = gridMat(gates)
    
    print(grid)


if __name__ == "__main__":
    main()
