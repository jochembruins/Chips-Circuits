# make objects per gate
class Location(object):
    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" % (self.gate, self.x, self.y, self.z)
