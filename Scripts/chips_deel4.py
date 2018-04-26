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

def routeFinder(gates, wire, grid):
    route = []
    locfrom = [gates[wire[0]].z, gates[wire[0]].y, gates[wire[0]].x]
    cursor = locfrom
    locto = [gates[wire[1]].z, gates[wire[1]].y, gates[wire[1]].x]
    # print(wire, locfrom, locto)
    # add begin point to route
    route.append([cursor[0], cursor[1], cursor[2]])
    # print(cursor)

    # look for best step until 1 step away from endpoint
    # HIER MOET EIGENLIJK NOG abs(locto[0] - cursor[0]) IN WHILE STATEMENT OM Z -AS TE CHECKEN
    # DIT WERKT NOG NIET, WORDT INFINITE LOOP, MOGELIJKE OPLOSSING ZIE ONDERAAN FUNCTIE MET RANDOMSTEP
    # MISSCHIEN OOK VOOR ALLE STAPJES EN ROUTE.APPEND IN LOSSE FUNCTIES
    while abs(locto[1] - cursor[1]) + abs(locto[2] - cursor[2]) > 1:

        # check if steps in y direction is bigger than x direction
        if abs(locto[1] - cursor[1]) > abs(locto[2] - cursor[2]):
            # step along y axis
            if locto[1] > cursor[1]:
                cursor[1] += 1
            else:
                cursor[1] -= 1
        else:
            # step along x axis
            if locto[2] > cursor[2]:
                cursor[2] += 1
            else:
                cursor[2] -= 1
        # save step in route
        route.append([cursor[0], cursor[1], cursor[2]])
        # print(cursor)

        # check if previous step is possible else delete and go up z-axis
        if grid[cursor[0], cursor[1], cursor[2]] != 99:
            # print([route[-1], "del"])
            del route[-1]
            # print(route[-1], "new cursor")
            cursor = [route[-1][0], route[-1][1], route[-1][2]]
            # print("up")
            cursor[0] += 1
            route.append([cursor[0], cursor[1], cursor[2]])
            # print(cursor)
        # if step down is possible, go down
        elif grid[cursor[0] - 1, cursor[1], cursor[2]] == 99.0 and cursor[0] > 0:
            # print("down")
            cursor[0] -= 1
            route.append([cursor[0], cursor[1], cursor[2]])
            # print(cursor)

        # make random step if stuck in infinite loop (does not work yet)
        # if len(route) >= 4 and route[-1] == route[-4]:
        #     randomstep = randint(1, 4)
        #     if randomstep == 1:
        #         cursor[1] += 1
        #     elif randomstep == 2:
        #         cursor[1] -= 1
        #     elif randomstep == 3:
        #         cursor[2] += 1
        #     else:
        #         cursor[2] -= 1
        #     route.append([cursor[0], cursor[1], cursor[2]])
        #     print("randomstep")

    # add end point to route
    route.append(locto)
    # print(locto)
    return route

