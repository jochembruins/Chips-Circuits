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
# pip3 install numpy
# pip3 install matplotlib

from numpy import genfromtxt
import matplotlib.pyplot as plt

gatesloc = genfromtxt('gates.csv', delimiter=';')

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
quit()

