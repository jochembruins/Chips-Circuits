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

# read gates data
gatesloc = genfromtxt('gates.csv', delimiter=';')

# make objects per gate
class Location(object):
    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" % (self.gate, self.x, self.y, self.z)

gates = []
for line in gatesloc:
    line = Location(line[0], int(line[1]), int(line[2]), int(line[3]))
    gates.append(line)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Define ticks
major_ticks = np.arange(0, 18, 1)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)

for obj in gates:
    plt.plot(obj.x, obj.y, 'ro')    # WAAR KOMEN FIG EN PLOT SAMEN?
    plt.annotate(int(obj.gate), xy=(obj.x, obj.y))

# And a corresponding grid
plt.grid(which='both')
plt.axis([0, 17, 12, 0])
plt.show()
quit()

