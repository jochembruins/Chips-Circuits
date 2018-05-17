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

import random

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

    # deze functie ordent de netlist
    # hierbij wordt er geordend op lengte van een netlistelementconnectie (blauwe lijn)
    # als argument wordt een netlist genomen + de gates
    def daltonMethod(netlist, gate):
        # tweede versie van netlist opgeslagen 
        netlistversion2 = netlist

        # lege derde versie van te definieren netlist opgeslagen
        netlistversion3 = []
        # lengte netlist berekend
        k = len(netlist)

        # itereren over lengte netlist
        for j in range(0, k):

            # het minimum worddt op een hoog getal gezet
            minimum = 1000
            # numbernetlist wordt 0
            numbernetlist = 0

            # itereren over lengte netlist min j
            for i in range(0, k - j):
                # de eerste factor van wire opslaan in listelement1
                listelement1 = netlistversion2[i][0]
                # de tweede factor van wire opslaan in listelement2
                listelement2 = netlistversion2[i][1]

                # verschil in x-waarden netconnecties opslaan in x_verschil
                x_verschil = abs(gate[listelement1].x - gate[listelement2].x)
                # verschil in y-waarden netconnecties opslaan in y_verschil
                y_verschil = abs(gate[listelement1].y - gate[listelement2].y)
                som = x_verschil + y_verschil

                # als de som van x_verschil en y_verschil kleiner dan minimum
                if (som < minimum):
                    minimum = som
                    numbernetlist = i

            # zet zojuist bepaalde netlistelement in netlistversion3
            netlistversion3.append(netlistversion2[numbernetlist])
            
            # haalde aangewezen element uit netlistversion2
            netlistversion2.pop(numbernetlist)

        # return nieuwe netlist
        return (netlistversion3)


    # deze functie ordent de netlist
    # hierbij wordt er geordend of een netlistelementconnectie (blauwe lijn) aan de buitenkant ligt
    # als argument wordt een netlist genomen + de gates
    def UIMethod_forprint1(netlist, gate):
        # tweede versie van netlist opgeslagen
        netlistversion2 = netlist
        # lege derde versie van te definiëren netlist opgeslagen
        netlistversion3 = []
        # lengte netlist berekend
        k = len(netlist)

        # de breedte van het eerste veld is 17 (tellend vanaf 0)
        breedte = 17
        # de hoogte van het eerste veld is 12 (tellend vanaf 0)
        hoogte = 12

        # helftbreedte en hoogte worden berekend om het bord te scheiden
        helftbreedte = breedte / 2
        helfthoogte = hoogte / 2

        # itereren over lengte netlist
        for j in range(0, k):
            # het minimum worddt op een hoog getal gezet
            minimum = 1000
            # numbernetlist wordt 0
            numbernetlist = 0

            # itereren over lengte netlist min j
            for i in range(0, k - j):
                # de eerste factor van wire opslaan in listelement1
                listelement1 = netlistversion2[i][0]
                # de tweede factor van wire opslaan in listelement2
                listelement2 = netlistversion2[i][1]

                # check of de x-waarde in de eerste helft valt
                if (gate[listelement1].x <= helftbreedte):
                    x1waarde = gate[listelement1].x
                else:
                    # anders wordt de waarde breedte minus x-element
                    x1waarde = breedte - gate[listelement1].x

                if (gate[listelement1].y <= helfthoogte):
                    y1waarde = gate[listelement1].y
                else:
                    y1waarde = hoogte - gate[listelement1].y

                # de waarde van de eerste gate is het minimum van de x1- en y1waarde
                waarde1 = min(x1waarde, y1waarde)

                if (gate[listelement2].x <= helftbreedte):
                    x2waarde = gate[listelement2].x
                else:
                    x2waarde = breedte - gate[listelement2].x

                if (gate[listelement2].y <= helfthoogte):
                    y2waarde = gate[listelement2].y
                else:
                    y2waarde = hoogte - gate[listelement2].y

                # de waarde van de tweede gate is het minimum van de x2- en y2waarde
                waarde2 = min(x2waarde, y2waarde)

                som = waarde1 + waarde2

                # als de som kleiner is dan het minimum
                if (som < minimum):
                    minimum = som
                    numbernetlist = i

            # zet zojuist bepaalde netlistelement in netlistversion3
            netlistversion3.append(netlistversion2[numbernetlist])
            # haalde aangewezen element uit netlistversion2
            netlistversion2.pop(numbernetlist)
        # return nieuwe netlist
        return (netlistversion3)


    def changeRouteBook(routeBook):
        
        # set indexes to zero
        index1 = 0
        index2 = 0

        # loop to make sure indexes are not the same
        while index1 == index2:
            index1 = random.randrange(0,len(routeBook))
            index2 = random.randrange(0,len(routeBook))

        # swap routes in routebook
        tmp = routeBook[index1]
        routeBook[index1] = routeBook[index2]
        routeBook[index2] = tmp

        return routeBook



