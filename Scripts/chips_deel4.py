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
import matplotlib.pyplot as plt

gatesloc = genfromtxt('../Data/gates.csv', delimiter=';')

class Location(object):
    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)


    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" % (self.gate, self.x, self.y, self.z)

gate = []
for line in gatesloc:
    line = Location(line[0], int(line[1]), int(line[2]), int(line[3]))
    gate.append(line)

for obj in gate:
    plt.plot(obj.y, obj.x, 'ro')
plt.axis([0, 17, 12, 0])
plt.grid()
plt.show()

# netlist inladen
# print 1
# lengte 30
netlist_1 = [(23, 4), (5, 7), (1, 2), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 2), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]


