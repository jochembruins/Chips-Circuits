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

import statistics
from copy import deepcopy
from time import time
import classes
import functions
import netlists
import pandas as pd
from progressbar import ProgressBar


def userInterface():
	""" Gebruik userinterface"""

	print("\n\nCHIPS & CIRCUITS\n"
		  "Welkom bij de programmeertheoriecase van de Veganboyz\n"
		  "(aka Melle Gelok, Jochem Bruins, Noah van Grinsven)\n")
	print("Wat zou je willen zien?\n"
		  "1: Los één van de 6 netlists op\n"
		  "2: Het effect van de volgorde van een netlists op het resultaat\n"
		  "3: De output van 'Breaktrough algoritme'\n"
		  "4: De output van 'Gewogen Astar' algoritme\n"
		  "5: Vergelijking van 3 verschillende hillclimbers")
	while (True):
		response1 = input("Maak een keuze: ")
		if str.isnumeric(response1) is False or int(response1) < 1 or int(
			response1) > 5:
			print("Dit is geen geldige input\n"
				  "Voorbeeld van geldige input is: 1, 2, 3, 4 of 5")
		else:
			break

	if response1 == '1' or response1 == '4':
		print("Kies uit netlist 1 - 6")

		while (True):
			response2 = input("Maak een keuze: ")
			if str.isnumeric(response2) is False or int(response2) > 6 or int(
				response1) < 1:
				print("Dit is geen geldige input\n"
					  "Voorbeeld van geldige input is: 1, 2, 3, 4, 5 of 6")
			else:
				break

		if response2 == '1':
			netlist = netlists.netlist_1
		elif response2 == '2':
			netlist = netlists.netlist_2
		elif response2 == '3':
			netlist = netlists.netlist_3
		elif response2 == '4':
			netlist = netlists.netlist_4
		elif response2 == '5':
			netlist = netlists.netlist_5
		else:
			netlist = netlists.netlist_6

	else:
		print("Kies uit netlist 1 - 3")
		while (True):
			response2 = input("Maak een keuze: ")
			if str.isnumeric(response2) is False or int(response2) > 3 or int(
				response2) < 1:
				print("Dit is geen geldige input\n"
					  "Voorbeeld van geldige input is: 1, 2 of 3")
			else:
				break

		if response2 == '1':
			netlist = netlists.netlist_1
		elif response2 == '2':
			netlist = netlists.netlist_2
		else:
			netlist = netlists.netlist_3

	return response1, response2, netlist


def solveNetlist(routeBook, grid, size, gates):
	""" Algoritme dat met behulp van A-star elke netlist kan oplossen"""

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
									  size, 600)

	# print info over uitkomsten
	print('Score na replaceLine: ', functions.getScore(NewRoutes[0]))
	print('Check op correctheid: ', functions.checker(NewRoutes[0]))
	print('Tip: draai plot door muis in te drukken en te bewegen.')

	# plot grafiek
	statistics.plotChip(gates, NewRoutes[0], size)


def compareNetlists(netlist, gates, routeBook, size, response, grid):
	""" Vergelijk verschillende netlists door ze met gewogen A-star
	op te lossen en met pure A-star te optimaliseren"""

	# maak netlists met Ui/Dalton methode
	netlistDalton = classes.wire.daltonMethod(netlist, gates)
	netlistUi = classes.wire.uiMethod(netlist, gates)

	# sla ingaande routebook van beste oplossing randomroute op
	randomRouteBookIn = functions.randomRouteBook(routeBook, gates,
												  size, response, 100)[
		0]
	randomRouteNetlistIn = []
	for object in randomRouteBookIn:
		randomRouteNetlistIn.append(object.netPoint)

	netlistCompare = [netlistDalton, netlistUi, randomRouteNetlistIn]

	# bereid voortgangsbar voor
	pbar = ProgressBar()

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
			compare = pd.concat([compare, routesBetter[1]], axis=1,
								join='inner')

		# info ingaande routeBook
		print("\nBeginstand netlist: ", netlist)
		netlistDist = functions.manhattanDist(routeBook)[1]
		print("Manhattan distance van netPoints: ", netlistDist)

		for object in routesBetter[0]:
			eindstandNetlist.append(object.netPoint)
		# print info over resultaten
		print("Eindstand netlist: ", eindstandNetlist)
		print("Manhattan distance van netPoints: ",
			  functions.manhattanDist(routesBetter[0])[1])

		print("score voor netlist =", functions.getScore(routesBetter[0]))
		# statistics.plotChip(gates, routesBetter[0], size)

		# reset grid
		grid = functions.gridMat(gates, size)

		toc = time()
		print('Runtime: ', toc - tic)

	# draai lijngrafiek uit om netlists te vergelijken
	compare.columns = ['Dalton', 'Ui', 'Random']
	statistics.plotLine(compare, 'Vergelijking sorteermethodes')


def compareHillClimbers(routeBook, gates, size, response, grid):
	""" Functie vergelijkt de Swap-2-Breaktrough-hillclimber met
	de hillclimber ReplaceLine (zowel willekeurig als op volgorde)"""

	# vind een werkend willekeurig routebook
	randomRouteBook = functions.randomRouteBook(routeBook, gates,
												size, response, 100)

	print("Score voor netlist =", randomRouteBook[1])

	# gebruik Swap-2-Breakthrough hillclimber
	HillClimber = functions.hillClimb(randomRouteBook[2], randomRouteBook[1],
									  gates, size, response, 1000)

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
	compare.columns = ['Hillclimber met Breakthrough', 'Replacelines op volgorde',
						   'Replacelines willekeurig']

	# plot lijngrafiek
	statistics.plotLine(compare, 'Hillclimber en Replacelines')


def breakThrough(routeBook, gates, chip, response):
	""" Vind een route voor met behulp van het breakThrough algoritme.
	Om verzekerd een route te geven, maken we gebruik van de functie 
	randomRouteBook."""

	tic = time()
	bestRoute = functions.randomRouteBook(routeBook, gates, chip, response, steps=1000)
	toc = time()

	print("Score voor netlist =", bestRoute[1])
	print('Check op correctheid: ', functions.checker(bestRoute[2]))
	print('Runtime: ', toc - tic)
	print('Tip: draai plot door muis in te drukken en te bewegen.')

	statistics.plotChip(gates, bestRoute[2], chip)


def weightedAStar(routeBook, gates, grid, chip):
	""" Vind een route met de gewogen A-star. Dit is dus een valide,
	maar geen geoptimaliseerde route"""

	tic = time()
	route = functions.aStarRouteFinder(routeBook, grid, chip)
	toc = time()

	print("Score voor netlist =", functions.getScore(route[0]))
	print('Check op correctheid: ', functions.checker(route[0]))
	print('Runtime: ', toc - tic)
	print('Tip: draai plot door muis in te drukken en te bewegen.')

	statistics.plotChip(gates, route[0], chip)
