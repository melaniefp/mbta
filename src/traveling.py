from dataStructures import Route, Stop

MAX_TRAVEL_CANDIDATES = 100

class Travel(object):
    """ one travel is one path (or edge) traversing 1 or more routes """

    def __init__(self, routes=[]): self.routes = routes

    @property
    def last_route(self): return self.routes[-1]

    @property
    def prev_routes(self): return self.routes[:-1]

    def _contains(self,route): return route.isIn(self.routes)

    def _copy(self):
        travel = Travel()
        travel.routes = self.routes.copy()
        return travel

    def _has_loop(self): return (self.last_route.isIn(self.prev_routes) )

    def reaches(self,destRoutes): return (self.last_route.isIn(destRoutes))

    def add(self,route):
        ''' only adds route if not already present in travel '''
        if not(self._contains(route)): self.routes.append(route)

    def info(self): return ', '.join([x.name for x in self.routes])

    def extend(self):

        lastRoute = self.last_route
        neighborRoutes = lastRoute.next()
        isNew = [not(self._contains(x)) for x in neighborRoutes]
        routesToAdd = [x for i,x in enumerate(neighborRoutes) if isNew[i] == True]

        if len(routesToAdd) == 0: return []

        else:

            extendedTravels = []
            for route in routesToAdd:
                travel = self._copy()
                travel.add(route)
                extendedTravels.append(travel)

            return extendedTravels

class TravelCandidates:
    ''' Container with all travel candidates '''

    def __init__(self):
        self.travels = []   # paths in graph

    @property
    def num_travels(self): return len(self.travels)

    @property
    def routes(self): # nodes in graph
        ''' which routes are present in container '''
        allRoutes = []
        for travel in self.travels: allRoutes += travel.routes

        seen = set()
        filteredRoutes = []
        for c in allRoutes:
            if c.name not in seen: filteredRoutes.append(c)
            seen.add(c.name)

        return filteredRoutes

    def _reached_from(self,travel): return travel.last_route.isIn(self.routes)

    def _isValid(self,travel):
        ''' an invalid travel reaches a route previously visited '''
        return not(self._reached_from(travel) or travel._has_loop() )

    def pop(self): return self.travels.pop(0)

    def add(self,travel):
        if self._isValid(travel): self.travels.append(travel)

    def extend(self, travel):
        ''' extend travel candidates by expanding current travel '''
        extendedTravels = travel.extend()
        for i,travel in enumerate(extendedTravels):
            if self._isValid(travel): self.add(travel)

    def isEmpty(self): return (self.num_travels == 0)

    def info(self): return [x.info() for x in self.travels]

if __name__ == '__main__':

    # testing of Travel Class

    routes = Route.get_subway_routes()
    travelA = Travel(routes)
    travelA.info()

    travelB = Travel()
    travelB.add(routes[0])

    travelC = travelB._copy()
    travelC.info()

    travelC.last_route

    assert (travelA.reaches([routes[-1]]) == True)
    assert (travelA.reaches([routes[0]]) == False)

    extendedTravels = travelC.extend()
    extendedTravels[0].info()

    # testing of TravelCandidates class

    tc = TravelCandidates()
    tc.add(travelA)
    print('OK')

