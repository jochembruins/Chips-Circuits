# python script
###########################################################
# options.py
#
# Jochem Bruins
# 10578811
#
# Melle Gelok
# 11017893
#
# Noah van Grinsven
# 10501917
#
# Chips & Circuits
#
# Bevat alle opties die kunnen worden opgeroepen 
# door de gebruiker
###########################################################

import functions
import statistics
import classes
from time import time
from progressbar import ProgressBar
from copy import deepcopy
import pandas as pd


def solveNetlist(routeBook, grid, size, gates):
	"""Algoritme dat met behulp van A-star elke netlist kan oplossen"""
	
	# Leg met gewogen A-star
	routes = functions.aStarRouteFinder(routeBook, grid, size)

    # print info over uitkomsten
    print('Score na gewogen aStarRouteFinder: ', functions.getScore(routes[0]))
    print('Check op correctheid: ', functions.checker(routes[0]))

    # maak nieuw grid adhv het beste gevonden routebook
    for route in routes[0]:
        grid = functions.changeMat(route.route, grid)

    # verbeter route door met pure A* lijnen opnieuw te leggen
    NewRoutes = functions.replaceLine(routes[0],
	                                 grid, 1,
	                                 size, 1000)

    # print info over uitkomsten
    print('Score na replaceLine: ', functions.getScore(NewRoutes[0]))
    print('Check op correctheid: ', functions.checker(NewRoutes[0]))

    #plot grafiek
    statistics.plotChip(gates, NewRoutes[0], size)


def compareNetlists(netlist, gates, routeBook, size, grid):
    """Vergelijk verschillende netlists door ze met gewogen A-star
	op te lossen en met pure A-star te optimaliseren"""
	
    # maak netlists met Ui/Dalton methode
    netlistDalton = classes.wire.daltonMethod(netlist, gates)
    netlistUi = classes.wire.uiMethod(netlist, gates)

    # sla ingaande routebook van beste oplossing randomroute op
    randomRouteBookIn = functions.randomRouteBook(routeBook, gates, size, 1000)[0]
    randomRouteNetlistIn = []
    for object in randomRouteBookIn:
        randomRouteNetlistIn.append(object.netPoint)

    netlistCompare = [netlistDalton, netlistUi, randomRouteNetlistIn]

    # bereid voortgangsbar voor
    pbar = ProgressBar()
    print("Hillclimber - replaceline algoritme")

    for netlist in pbar(netlistCompare):
        tic = time()

        # maar variabel aan
        eindstandNetlist = []

        # maak object van iedere netPoint, maak lijst van alle netPoints
        routeBook = functions.makeObjects(netlist, gates)
        routeBookEmpty = deepcopy(routeBook)

        # leg routes met gewogen Astar algoritme
        routesFound = functions.aStarRouteFinder(routeBookEmpty, grid, size)

        # maak nieuw grid adhv het beste gevonden routebook
        for route in routesFound[0]:
            grid = functions.changeMat(route.route, grid)

        # verbeter route door met pure A* lijnen opnieuw te leggen
        routesBetter = functions.replaceLine(routesFound[0], grid, 0, size, 500)

	    
        if netlistCompare.index(netlist) == 0:
            compare = routesBetter[1]
        else:
            compare = pd.concat([compare, routesBetter[1]], axis=1, join='inner')

        # info ingaande routeBook
        print("\nBeginstand netlist: ", netlist)
        netlistDist = functions.manhattanDist(routeBook)[1]
        print("Manhattan distance van netPoints: ", netlistDist)

        for object in routesBetter[0]:
            eindstandNetlist.append(object.netPoint)
        # print info over resultaten
        print("Eindstand netlist: ", eindstandNetlist)
        print("Manhattan distance van netPoints: ", functions.manhattanDist(routesBetter[0])[1])

        print("score voor netlist =", functions.getScore(routesBetter[0]))
        # statistics.plotChip(gates, routesBetter[0], size)

        # reset grid
        grid = functions.gridMat(gates, size)

        toc = time()
        runtime = toc - tic
        print("runtime:", runtime)

    # draai lijngrafiek uit om netlists te vergelijken
	compare.columns = ['Dalton', 'Ui', 'Random']
    statistics.plotLine(compare, 'Vergelijking sorteermethodes')


def compareHillClimbers(routeBook, gates, size, grid):
    """ Functie vergelijkt de Swap-2-Breaktrough-hillclimber met
	de hillclimber ReplaceLine (zowel willekeurig als op volgorde)"""
	
    # vind een werkend willekeurig routebook
	randomRouteBook = functions.randomRouteBook(routeBook, gates, size, 100)
    #maak nieuw grid adhv het beste gevonden routebook

	# HILLCLIMBER: WISSEL TWEE NETPOINTS, LEG HELE NETLIST OPNIEUW ----------
	# laat hilclimber werken
	HillClimber = functions.hillClimb(randomRouteBook[2], randomRouteBook[1] , gates, size, 1000)

    # sla data op om HillClimbers te vergelijken
	compare = HillClimber[2]

    # verkrijg kloppende grid
	for route in randomRouteBook[2]:
        grid = functions.changeMat(route.route, grid)

    # verbeter route door met pure A* lijnen opnieuw te leggen
	# eerst in volgorde van de routeboek, daarna op willekeurige volgorde
    for i in range(0, 2):
        # maak deepcopy zodat we de routeboek twee keer kunnen gebruiken
	    routeBook = deepcopy(randomRouteBook[2])
	    
        # verkrijg kloppende grid
	    for route in randomRouteBook[2]:
	        grid = functions.changeMat(route.route, grid)
	    
	    # verbeter met replaceLine
	    NewRoute = functions.replaceLine(routeBook, grid, i, size, 1000)
	    
	    # voeg de data bij elkaar
	    compare = pd.concat([compare, NewRoute[1]], axis=1, join='inner')

	# verander namen columns
	compare.columns = ['Hillclimber met Breakthrough', 'Replacelines op volgorde', 'Replacelines willekeurig']

	# plot lijngrafiek
	statistics.plotLine(compare, 'Hillclimber en Replacelines')


>>>>>>> 58ca4916aee91342b6f3ece2983e46c28acdf2b7
