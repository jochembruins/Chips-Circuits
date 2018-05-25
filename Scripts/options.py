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

def solveNetlist(routeBook, grid, size):
	# Leg met gewogen A-star
	routes = functions.aStarRouteFinder(routeBook, grid, size)

	# check validiteit
	print(functions.checker(routes[0]))

	#bereken score
	print(functions.getScore(routes[0]))

	# maak nieuw grid adhv het beste gevonden routebook
	for route in routes[0]:
	    grid = functions.changeMat(route.route, grid)

	# verbeter route door met pure A* lijnen opnieuw te leggen
	NewRoutes = functions.replaceLine(routes[0],
	                                 grid, 0,
	                                 size, 1000)

	# print info over uitkomsten
	print(functions.getScore(NewRoutes[0]))
	print(functions.checker(NewRoutes[0]))

	#plot grafiek
	statistics.plotChip(gates, NewRoute[0], size)