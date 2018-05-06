# python script
###########################################################
# classes.py
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
#
# Contains all classes used in chips.py
###########################################################

# make objects per gate
class Location(object):
    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" % (self.gate, self.x, self.y, self.z)

class wire(object):
    def __init__(self, netPoint, locFrom, locTo, fromSurround, toSurround, route):
        self.netPoint = netPoint
        self.locFrom = locFrom
        self.locTo = locTo
        self.fromSurround = fromSurround
        self.toSurround = toSurround
        self.route = route

    def __str__(self):
        return "netPoint: %s, locFrom: %s, locTo: %s, fromSurround: %s toSurround: %s route: %s" % \
               (self.netPoint, self.locFrom, self.locTo, self.fromSurround, self.toSurround, self.route)
