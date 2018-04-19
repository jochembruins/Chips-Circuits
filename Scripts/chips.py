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
# instalrequirements:
# pip3 install numpy
# pip3 install matplotlib

from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import classes.py
import functions.py

def main():
    # read gates data
    gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')
    
    gates = makeLocations(gatesloc)
    
    printPlot(gates)

    grid = gridMat(gates)
    
    print(grid)
    


if __name__ == "__main__":
    main()
