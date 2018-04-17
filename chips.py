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
gatesloc = genfromtxt('gates.csv', delimiter=';')

print(gatesloc)

plot = []
for line in gatesloc:
    plot.append({
        'gate': int(line[0]),
        'x': int(line[1]),
        'y': int(line[2]),
        'z': int(line[3])})


class location(object):
    def __init__(self, gate, x, y, z):
        self.__dict__ = self
        self.gate = gate
        self.x = x
        self.y = y
        self.z = z

grid = []
for line in gatesloc:
    grid[location.x,location.y] = 1