def aStarRouteFinder (routeBook, grid):
    """ Functie zoekt naar valide oplossing met gewogen Astar """
    
    # maak benodige variabelen aan
    tic = time()
    
    # lege grid
    gridEmpty = deepcopy(grid)
    
    # lijst met routes die nog gelegd moeten worden
    routeBookEmpty = deepcopy(routeBook)
    
    # nog lege lijst te vullen met gelegde routes
    routeBookDone = []
    
    # lijst om geslaagde netlist op te slaan
    routeBookSolved = deepcopy(routeBook)
    
    # counter voor het aantal iteraties
    loops = 0

    # loop totdat de routeboek leeg is
    while routeBookEmpty != []:
        # loop over alle elementen in de routeboek
        for netPoint in routeBookEmpty:
    
            # houd aantal loops bij
            loops += 1

            # controleert of de begingate van de lijn is ingesloten
            count = 0
            for loc in netPoint.fromSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            
            # verwijdert onnodige lijnen indien ingesloten
            if count == 5:
                routeBookEmpty, routeBookDone, grid = searchLocFrom(netPoint, routeBookEmpty, routeBookDone, grid)[0:3]   

            # controleert of de begingate van de lijn is ingesloten
            count = 0
            for loc in netPoint.toSurround:
                if grid[loc[0], loc[1], loc[2]] != 99:
                    count += 1
            
            # verwijdert onnodige lijnen indien ingesloten
            if count == 5:
                routeBookEmpty, routeBookDone, grid = searchLocTo(netPoint, routeBookEmpty, routeBookDone, grid)[0:3] 

            # leg de route met Astar
            route = aStar(netPoint, grid, 2, 'groot')

            # voeg nieuwe route toe aan netPoins als Astar succesvol is
            if route != []:
                netPoint.route = route
                
                # update grid
                grid = changeMat(route, grid)

                # verplaats van 'emtpy-' naar 'done-' lijst
                doneWire = routeBookEmpty.pop(routeBookEmpty.index(netPoint))
                routeBookDone.append(doneWire)
            
            # begin opnieuw als maximaal aantal loops is bereikt
            if loops == 150:
                lengthEmpty = len(routeBookEmpty)
                print(lengthEmpty)
                routeBookEmpty = routeBookEmpty + routeBookDone
                routeBookDone = []
                loops = 0
                
                # alleen shuffelen als de er meer dan vier routes onopgelost bleven
                if lengthEmpty > 4:
                    print('shuffle')
                    shuffle(routeBookEmpty)
                    
                # update laatste routeBook 
                print('update')
                routeBookSolved = deepcopy(routeBookEmpty)

                # maak grid weer leeg
                grid = deepcopy(gridEmpty)
                
    # bereken tijd
    toc = time()
    print(toc-tic)
                
     # check validiteit
    print(checker(routeBookDone))
    
    # krijg score
    print(getScore(routeBookDone))
    
    return routeBookDone, routeBookSolved