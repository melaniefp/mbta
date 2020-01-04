import json
import requests

import pdb

ROUTES_API = "https://api-v3.mbta.com/routes"
STOPS_API = "https://api-v3.mbta.com/stops"

class DataRetriever:
    ''' class to retrieve data from MBTA server '''

    # TODO: caché dictionaries to retrieve route and stop objs faster
    routeRegister = dict()
    stopRegister = dict()

    def _get_json(fromPath,params=dict()):
        ''' basic curl query to retrieve json, depends of ext API '''
        response = requests.get(fromPath,params)
        jsonResponse = response.json()
        return jsonResponse

    @classmethod
    def get_jsonRoutes(cls, stopId):
        params = {
                'filter[stop]': stopId,
                'include': 'stop',
                }
        jsonStr = cls._get_json(ROUTES_API, params)
        jsonRoutes = [JsonRoute(x) for x in jsonStr['data']]
        return jsonRoutes

    @classmethod
    def get_jsonStops(cls, routeId):
        params = {
                'filter[route]': routeId,
                'include': 'route',
                }
        jsonStr = cls._get_json(STOPS_API, params)
        jsonStops = [JsonStop(x) for x in jsonStr['data']]
        return jsonStops

class JsonStop:

    def __init__(self,jsonStop): self.json = jsonStop

    @property
    def id(self): return self.json['id']

    @property
    def name(self): return self.json['attributes']['name']

class JsonRoute:

    def __init__(self,jsonRoute): self.json = jsonRoute

    @property
    def id(self): return self.json['id']

    @property
    def name(self): return self.json['attributes']['long_name']

if __name__ == '__main__':

    # test for basic query
    jsonRoutes = DataRetriever._get_json(ROUTES_API)
    print(jsonRoutes['data'][0])
    print('\n')

    stopId = 'place-pktrm'
    jsonRoutes = DataRetriever.get_jsonRoutes(stopId)
    print('{}: {}'.format(jsonRoutes[0].id, jsonRoutes[0].name))
    print('\n')

    routeId = 'Green-E'
    jsonStops = DataRetriever.get_jsonStops(routeId)
    print('{}: {}'.format(jsonStops[0].id, jsonStops[0].name))
    print('\n')
