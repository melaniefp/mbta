class Subway:
    ''' class to contain static information on stops and routes '''

    def __init__(self, routes, stops, stop2routes, route2stops):
        self.routes = routes
        self.stops = stops
        self.stop2routes = stop2routes
        self.route2stops = route2stops

    def get_route(self, key): return self.routes[key]

    def get_stop(self, key): return self.stops[key]

    def get_routeIds(self, stop):
        if type(stop) == str: stop = self.stops[stop]
        return self.stop2routes[stop.id]

    def get_stopIds(self, route):
        if type(route) == str: route = self.routes[route]
        return self.route2stops[route.id]

    def get_routes(self, stop):
        if type(stop) == str: stop = self.stops[stop]
        routeIds = self.get_routeIds(stop)
        return [self.routes[x] for x in routeIds]

    def get_stops(self, route):
        if type(route) == str: route = self.routes[route]
        stopIds = self.get_stopIds(route)
        return [self.stops[x] for x in stopIds]

    def get_all_routes(self): return list(self.routes.values())

    def get_all_stops(self): return list(self.stops.values())

    def get_next_routeIds(self, route):
        ''' returns routes connected to route '''

        if type(route) == str: route = self.routes[route]
        stopIds = self.get_stopIds(route.id)

        routeIds = []
        for stopId in stopIds: routeIds += self.get_routeIds(stopId)

        routeIds = list(set(routeIds))
        try:
            routeIds.remove(route.id)
        except:
            True

        return routeIds

    def get_next_routes(self, route):
        routeIds = self.get_next_routeIds(route)
        nextRoutes = []
        for routeId in routeIds: nextRoutes.append(self.get_route(routeId))

        return nextRoutes

    @classmethod
    def isIn(cls,route, routes):
        return (route.name in [x.name for x in routes])
