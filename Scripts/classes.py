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
from copy import deepcopy


class Location(object):
    """ maak objecten voor de gate locaties """

    def __init__(self, gate, x, y, z):
        self.gate = gate
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __str__(self):
        return "gate: %i, x: %i, y: %i, z: %i" \
               % (self.gate, self.x, self.y, self.z)


class wire(object):
    """ maak objecten voor iedere netPoint in de netlist """

    def __init__(self, netPoint, locFrom, locTo, fromSurround, toSurround, route):
        self.netPoint = netPoint
        self.locFrom = locFrom
        self.locTo = locTo
        self.fromSurround = fromSurround
        self.toSurround = toSurround
        self.route = route

    def __str__(self):
        return "netPoint: %s, locFrom: %s, locTo: %s, " \
               "fromSurround: %s toSurround: %s route: %s" % \
               (self.netPoint, self.locFrom, self.locTo,
                self.fromSurround, self.toSurround, self.route)

    def daltonMethod(netlist, gate):
        """ deze functie ordent de netlist hierbij wordt er geordend op lengte
            van een netlistelementconnectie (blauwe lijn)
            als argument wordt een netlist genomen en de gates data """

        # tweede versie van netlist opgeslagen
        netlistVersion2 = deepcopy(netlist)

        # lege derde versie van te definieren netlist opgeslagen
        netlistVersion3 = []
        # lengte netlist berekend
        k = len(netlist)
        # itereren over lengte netlist
        for j in range(0, k):

            # het minimum wordt op een hoog getal gezet
            minimum = 1000
            # numbernetlist wordt 0
            numbernNetlist = 0

            # itereren over lengte netlist min j
            for i in range(0, k - j):
                # de eerste factor van wire opslaan in listelement1
                listElement1 = netlistVersion2[i][0]
                # de tweede factor van wire opslaan in listelement2
                listElement2 = netlistVersion2[i][1]

                # verschil in x-waarden netconnecties opslaan in x_verschil
                x_difference = abs(gate[listElement1].x - gate[listElement2].x)
                # verschil in y-waarden netconnecties opslaan in y_verschil
                y_difference = abs(gate[listElement1].y - gate[listElement2].y)
                sum = x_difference + y_difference

                # als de som van x_verschil en y_verschil kleiner dan minimum
                if (sum < minimum):
                    minimum = sum
                    numbernNetlist = i

            # zet zojuist bepaalde netlistelement in netlistversion3
            netlistVersion3.append(netlistVersion2[numbernNetlist])
            
            # haalde aangewezen element uit netlistversion2
            netlistVersion2.pop(numbernNetlist)

        # return nieuwe netlist
        return netlistVersion3

    def uiMethod(netList, gate):
        """ deze functie ordent de netlist, hierbij wordt er geordend op
            hoe ver netlistelementconnecties aan de buitenkant
            van de grid liggen """

        # tweede versie van netlist opgeslagen
        netlistVersion2 = deepcopy(netList)
        # lege derde versie van te definiëren netlist opgeslagen
        netlistVersion3 = []
        # lengte netlist berekend
        k = len(netList)

        # de breedte van het eerste veld is 17 (tellend vanaf 0)
        width = 17
        # de hoogte van het eerste veld is 12 (tellend vanaf 0)
        height = 12

        # helftbreedte en hoogte worden berekend om het bord te scheiden
        halfWidth = width / 2
        halfHeight = height / 2

        # itereren over lengte netlist
        for j in range(0, k):
            # het minimum worddt op een hoog getal gezet
            minimum = 1000
            # numbernetlist wordt 0
            numberNetList = 0

            # itereren over lengte netlist min j
            for i in range(0, k - j):
                # de eerste factor van wire opslaan in listelement1
                listElement1 = netlistVersion2[i][0]
                # de tweede factor van wire opslaan in listelement2
                listElement2 = netlistVersion2[i][1]

                # check of de x-waarde in de eerste helft valt
                if (gate[listElement1].x <= halfWidth):
                    x1Value = gate[listElement1].x
                else:
                    # anders wordt de waarde breedte minus x-element
                    x1Value = width - gate[listElement1].x

                if (gate[listElement1].y <= halfHeight):
                    y1value = gate[listElement1].y
                else:
                    y1value = height - gate[listElement1].y

                # de waarde van de eerste gate is het
                # minimum van de x1- en y1waarde
                value1 = min(x1Value, y1value)

                if (gate[listElement2].x <= halfWidth):
                    x2Value = gate[listElement2].x
                else:
                    x2Value = width - gate[listElement2].x

                if (gate[listElement2].y <= halfHeight):
                    y2Value = gate[listElement2].y
                else:
                    y2Value = height - gate[listElement2].y

                # de waarde van de tweede gate is het
                # minimum van de x2- en y2waarde
                value2 = min(x2Value, y2Value)

                sum = value1 + value2

                # als de som kleiner is dan het minimum
                if (sum < minimum):
                    minimum = sum
                    numberNetList = i

            # zet zojuist bepaalde netlistelement in netlistVersion3
            netlistVersion3.append(netlistVersion2[numberNetList])
            # haalde aangewezen element uit netlistVersion2
            netlistVersion2.pop(numberNetList)
        # return nieuwe netlist
        return netlistVersion3

    def changeRouteBook(routeBook):
        
        # set indexes to zero
        index1 = 0
        index2 = 0

        # loop to make sure indexes are not the same
        while index1 == index2:
            index1 = random.randrange(0, len(routeBook))
            index2 = random.randrange(0, len(routeBook))

        # swap routes in routebook
        tmp = routeBook[index1]
        routeBook[index1] = routeBook[index2]
        routeBook[index2] = tmp

        return routeBook
