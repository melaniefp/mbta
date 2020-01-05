import json
import requests

from utils import cache

import pdb

ROUTES_API = "https://api-v3.mbta.com/routes"
STOPS_API = "https://api-v3.mbta.com/stops"

#def apiKey(func):
#    def wrapper_add_api_key(params, *args, **kwargs):
#        try:
#            params.update({'api_key':'a2945720cf954e53a9935a6803d4d7b8'})
#        except:
#            import pdb; pdb.set_trace()
#        func(*args,**kwargs)
#    return wrapper_add_api_key

class DataRetriever:
    ''' class to retrieve data from MBTA server '''

    # TODO: caché dictionaries to retrieve route and stop objs faster
    # instance variables
    routeRegister = dict()
    stopRegister = dict()

    def _get_json(fromPath,params=dict()):
        ''' basic curl query to retrieve json, depends of ext API '''
        response = requests.get(fromPath,params)
        jsonResponse = response.json()
        return jsonResponse

    @classmethod
    def get_jsonRoutes(cls, stopId=None, filterType=None):
        if stopId is None: # retrieve all
            # TODO: Remove hard-code wiring of API_KEY
            params = {
                'api_key':'a2945720cf954e53a9935a6803d4d7b8',
                    }
        else:
            params = {
                'filter[stop]': stopId,
                'include': 'stop',
                'api_key':'a2945720cf954e53a9935a6803d4d7b8',
                }
        if filterType is not None: params['filter[type]'] = filterType
        jsonStr = cls._get_json(ROUTES_API, params)
        try:
            jsonRoutes = [JsonRoute(x) for x in jsonStr['data']]
        except:
            raise ValueError('could not retrieve jsonRoutes')
        return jsonRoutes

    @classmethod
    @cache
    def get_jsonStops(cls, routeId=None):
        if routeId is None: # retrieve all
            params = {
                'api_key':'a2945720cf954e53a9935a6803d4d7b8',
                    } # retrieve all stops
        else:
            params = {
                'filter[route]': routeId,
                'include': 'route',
                'api_key':'a2945720cf954e53a9935a6803d4d7b8',
                }
        jsonStr = cls._get_json(STOPS_API, params)
        # TODO: Add throw Exception if jsonStr has no data
        try:
            jsonStops = [JsonStop(x) for x in jsonStr['data']]
        except:
            raise ValueError('could not retrieve jsonStops')

        return jsonStops

    @classmethod
    @cache
    def get_subway_jsonRoutes(cls, stopId=None):
        jsonRoutes = cls.get_jsonRoutes(stopId=stopId, filterType=0)
        jsonRoutes += cls.get_jsonRoutes(stopId=stopId, filterType=1)
        return jsonRoutes

    @classmethod
    @cache
    def get_subway_jsonStops(cls):
        jsonRoutes = cls.get_subway_jsonRoutes()
        routeIds = [x.id for x in jsonRoutes]
        jsonStops = []
        for routeId in routeIds:
            jsonStops += cls.get_jsonStops(routeId=routeId)

        # remove duplicated stops TODO: clean code
        stopIds = [x.id for x in jsonStops]
        uniqueStopIds = list(set(stopIds))
        selectIdxs = [stopIds.index(x) for x in uniqueStopIds]
        selectedJsonStops = [jsonStops[i] for i in selectIdxs]
        return selectedJsonStops

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

    ###

    stopId = 'place-pktrm'
    jsonRoutes = DataRetriever.get_jsonRoutes(stopId, filterType=0)
    print('{}: {}'.format(jsonRoutes[0].id, jsonRoutes[0].name))
    print('\n')

    jsonRoutes = DataRetriever.get_jsonRoutes(filterType=0)
    print('There are {} routes'.format(len(jsonRoutes)))
    print('\n')

    ###

    jsonRoutes = DataRetriever.get_jsonRoutes()
    print('There are {} routes'.format(len(jsonRoutes)))
    print('\n')

    jsonStops = DataRetriever.get_jsonStops()
    print('There are {} stops'.format(len(jsonStops)))
    print('\n')

    ##
    subwayRoutes = DataRetriever.get_subway_routes()
    assert (len(subwayRoutes) == 8)
    print('Number of subway routes: {}'.format(len(subwayRoutes)) )

    print('\nTESTS SUCCESSFUL')
