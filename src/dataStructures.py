from dataRetriever import DataRetriever
from dataRetriever import DataStop, DataRoute

from utils import cache, cached_property, memoize, Memoize

def from_dataObj(klass,dataObj):
    ''' from dataObj, create object '''
    if type(dataObj) == list:
        return [from_dataObj(klass, x) for x in dataObj]
    else:
        obj = klass(
            dataObj.id,
            dataObj.name,
            )
        return obj

dr = DataRetriever()

class Stop:

    storage = dict()

    def __init__(self, stopId, name):
        self.id = stopId
        self.name = name
        if name not in Stop.storage: Stop.storage[name] = self

    @cached_property
    def routes(self):
        dataRoutes = dr.get_subway_dataRoutes(stopId=self.id)
        routes = [Route.from_data(x) for x in dataRoutes]
        assert (len(routes) >= 1)
        return routes

    @property
    def num_routes(self): return len(self.routes)

    @classmethod
    def from_data(cls,dataStop):
        ''' from dataStop object, create Stop object '''
        return from_dataObj(cls,dataStop)

    @classmethod
    def get_subway_stops(cls):
        dataStops = dr.get_subway_dataStops()
        stops = cls.from_data(dataStops)
        return stops

    @classmethod
    def get(cls,stopId):
        try:
            return cls.storage[stopId]
        except:
            raise ValueError('Stop object has not been stored')

#@memoize
# TODO: singleton instance class
class Route:

    storage = dict()

    def __init__(self, routeId, name):
        self.id = routeId
        self.name = name
        if name not in Route.storage: Route.storage[name] = self

    @cached_property
    def stops(self):
        dataStops = dr.get_dataStops(self.id)
        stops = [Stop.from_data(x) for x in dataStops]
        assert (len(stops) >= 1)
        return stops

    @property
    def num_stops(self): return len(self.stops)

    @classmethod
    def from_data(cls,dataRoute):
        ''' from dataRoute object, create Route object '''
        return from_dataObj(cls,dataRoute)

    @classmethod
    def get_subway_routes(cls):
        dataRoutes = dr.get_subway_dataRoutes()
        routes = cls.from_data(dataRoutes)
        return routes

    @classmethod
    def get(cls,routeId):
        try:
            return cls.storage[routeId]
        except:
            raise ValueError('Route object has not been stored')

    @cache
    def next(self):
        ''' returns connected Routes via hub connections, except own route '''

        connectedRoutes = []
        # TODO: only add unique values
        for stop in self.stops: connectedRoutes += stop.routes
        routeNames = [x.name for x in connectedRoutes]
        routeNames.remove(self.name)

        # remove douplicated routes
        uniqueRouteNames = list(set(routeNames))
        uniqueIdxs = [routeNames.index(x) for x in uniqueRouteNames]
        filteredRouteNames = [routeNames[i] for i in uniqueIdxs]
        filteredRoutes = [connectedRoutes[i] for i in uniqueIdxs]

        return filteredRoutes

    def isIn(self,routes):
        return (self.name in [x.name for x in routes])


if __name__ == '__main__':

    # create stop
    stop = Stop('place-pktrm','Park Street')
    assert(stop.num_routes == 5)

    # create route
    route = Route('Red','Red Line')
    print(route.stops)
    print(route.num_stops)
