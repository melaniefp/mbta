import json
import requests
import os

from utils import cache

import pdb

DEFAULT_HOST = 'https://api-v3.mbta.com/'

class DataRetriever:
    ''' class to retrieve data from MBTA server '''

    def __init__(self, key='a2945720cf954e53a9935a6803d4d7b8', host=DEFAULT_HOST):

        self.host = host
        self.key = key
        self.routes_api = os.path.join(self.host,'routes')
        self.stops_api = os.path.join(self.host,'stops')

    def _get_json(self, fromPath,params=dict()):
        ''' basic curl query to retrieve json, depends of ext API '''
        response = requests.get(fromPath,params)
        jsonResponse = response.json()
        return jsonResponse

    @cache
    def get_dataRoutes(self, stopId=None, filterType=None):
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
    def get_dataStops(self, routeId=None):
        if routeId is None: params = {}
        else:
            params = {
                'filter[route]': routeId,
                'include': 'route',
                }
        if self.key is not None: params.update({'api_key': self.key})
        jsonStr = self._get_json(self.stops_api, params)
        # TODO: Add throw Exception if jsonStr has no data
        try:
            dataStops = [DataStop(x) for x in jsonStr['data']]
        except:
            raise ValueError('could not retrieve dataStops')

        return dataStops

    @cache
    def get_subway_dataRoutes(self, stopId=None):
        dataRoutes = self.get_dataRoutes(stopId=stopId, filterType=0)
        dataRoutes += self.get_dataRoutes(stopId=stopId, filterType=1)
        return dataRoutes

    @cache
    def get_subway_dataStops(self):
        dataRoutes = self.get_subway_dataRoutes()
        routeIds = [x.id for x in dataRoutes]
        dataStops = []
        for routeId in routeIds:
            dataStops += self.get_dataStops(routeId=routeId)

        # remove duplicated stops TODO: clean code
        stopIds = [x.id for x in dataStops]
        uniqueStopIds = list(set(stopIds))
        selectIdxs = [stopIds.index(x) for x in uniqueStopIds]
        selectedDataStops = [dataStops[i] for i in selectIdxs]
        return selectedDataStops

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

    stopId = 'place-pktrm'
    dataRoutes = dr.get_dataRoutes(stopId)
    print('{}: {}'.format(dataRoutes[0].id, dataRoutes[0].name))
    print('\n')

    routeId = 'Green-E'
    dataStops = dr.get_dataStops(routeId)
    print('{}: {}'.format(dataStops[0].id, dataStops[0].name))
    print('\n')

    ###

    stopId = 'place-pktrm'
    dataRoutes = dr.get_dataRoutes(stopId, filterType=0)
    print('{}: {}'.format(dataRoutes[0].id, dataRoutes[0].name))
    print('\n')

    dataRoutes = dr.get_dataRoutes(filterType=0)
    print('There are {} routes'.format(len(dataRoutes)))
    print('\n')

    ###

    dataRoutes = dr.get_dataRoutes()
    print('There are {} routes'.format(len(dataRoutes)))
    print('\n')

    dataStops = dr.get_dataStops()
    print('There are {} stops'.format(len(dataStops)))
    print('\n')

    ##
    dataRoutes = dr.get_subway_dataRoutes()
    assert (len(dataRoutes) == 8)
    print('Number of subway routes: {}'.format(len(dataRoutes)) )

    print('\nTESTS SUCCESSFUL')
