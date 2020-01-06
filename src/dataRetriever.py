import json
import requests
import os

from utils import cache
from subway import Subway

DEFAULT_HOST = 'https://api-v3.mbta.com/'
DEFAULT_KEY = 'a2945720cf954e53a9935a6803d4d7b8'

class DataRetriever:
    ''' class to retrieve data from MBTA server '''

    def __init__(self, key=DEFAULT_KEY, host=DEFAULT_HOST):

        self.host = host
        self.key = key
        self.routes_api = os.path.join(self.host,'routes')
        self.stops_api = os.path.join(self.host,'stops')

    def _get_json(self, fromPath,params=dict()):
        ''' basic HTTP query '''
        response = requests.get(fromPath,params)
        jsonResponse = response.json()
        # TODO: handle Exceptions
        return jsonResponse

    @cache
    def _get_dataRoutes(self, stopId=None, filterType=None):
        if stopId is None: params = {} # retrieve all
        else: # retrieve routes per stop
            params = {
                'filter[stop]': stopId,
                'include': 'stop',
                }
        if self.key is not None: params.update({'api_key': self.key})
        if filterType is not None: params['filter[type]'] = filterType
        jsonStr = self._get_json(self.routes_api, params)
        try:
            dataRoutes = [DataRoute(x) for x in jsonStr['data']]
        except:
            raise ValueError('could not retrieve dataRoutes')
        return dataRoutes

    @cache
    def _get_dataStops(self, routeId=None):
        if routeId is None: params = {}
        else:
            params = {
                'filter[route]': routeId,
                'include': 'route',
                }
        if self.key is not None: params.update({'api_key': self.key})
        jsonStr = self._get_json(self.stops_api, params)
        try:
            dataStops = [DataStop(x) for x in jsonStr['data']]
        except:
            raise ValueError('could not retrieve dataStops')

        return dataStops

    @cache
    def get_subway_dataRoutes(self, stopId=None):
        dataRoutes = self._get_dataRoutes(stopId=stopId, filterType=0)
        dataRoutes += self._get_dataRoutes(stopId=stopId, filterType=1)
        return dataRoutes

    @cache
    def get_subway_dataStops(self):
        dataRoutes = self.get_subway_dataRoutes()

        routeIds = [x.id for x in dataRoutes]
        aggregatedDataStops = []
        for routeId in routeIds:
            aggregatedDataStops += self._get_dataStops(routeId=routeId)

        # remove duplicated stops
        seen = set()
        dataStops = []
        for stop in aggregatedDataStops:
            if stop.name not in seen: dataStops.append(stop)
            seen.add(stop.name)

        return dataStops

    def get_subway(self):
        routeList = self.get_subway_dataRoutes()
        routes = dict()
        for route in routeList: routes[route.id] = route

        stopList = self.get_subway_dataStops()
        stops = dict()
        for stop in stopList: stops[stop.id] = stop

        route2stops = dict()
        for route in routeList:
            stopIds = [x.id for x in self._get_dataStops(routeId=route.id)]
            route2stops[route.id] = stopIds

        stop2routes = dict()
        for stop in stopList:
            routesPerStop = self.get_subway_dataRoutes(stopId=stop.id)
            routeIds = [x.id for x in routesPerStop]
            stop2routes[stop.id] = routeIds

        subway = Subway(routes, stops, stop2routes, route2stops)

        return subway


class DataStop:

    def __init__(self,json): self.json = json

    @property
    def id(self): return self.json['id']

    @property
    def name(self): return self.json['attributes']['name']

class DataRoute:

    def __init__(self,json): self.json = json

    @property
    def id(self): return self.json['id']

    @property
    def name(self): return self.json['attributes']['long_name']

if __name__ == '__main__':

    # test for basic query

    dr = DataRetriever()
    subway = dr.get_subway()

    stops = subway.get_all_stops()
    for stop in stops:
        print('{}: {}'.format(stop.id,stop.name))
