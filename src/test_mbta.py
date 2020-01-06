from dataRetriever import DataRetriever
from collections import namedtuple

from subway import Subway

from pathFinder import get_travel

Stop = namedtuple('Stop','id name')
Route = namedtuple('Route','id name')

def test_get_routes():
    dr = DataRetriever()
    stopId = 'place-pktrm'
    dataRoutes = dr._get_dataRoutes(stopId)
    print('{}: {}'.format(dataRoutes[0].id, dataRoutes[0].name))
    assert (dataRoutes[0].id == 'Red')
    assert (dataRoutes[0].name == 'Red Line')

### TEST SUBWAY CLASS

def create_dummy_subway():
    routes = {
            'R1': Route('R1','route1'),
            'R2': Route('R2','route2'),
            'R3': Route('R3','route3'),
            }
    stops = {
            'S1': Stop('S1','stop1'),
            'S2': Stop('S2','stop2'),
            'S3': Stop('S3','stop3'),
            'S4': Stop('S4','stop4'),
            'S5': Stop('S5','stop5'),
            'S6': Stop('S6','stop6'),
            'S7': Stop('S7','stop7'),
            }
    stop2routes = {
            'S1': ['R1'],
            'S2': ['R1','R3'],
            'S3': ['R1','R2'],
            'S4': ['R1'],
            'S5': ['R2'],
            'S6': ['R2','R3'],
            'S7': ['R2'],
            }
    route2stops = {
            'R1': ['S1','S2','S3','S4'],
            'R2': ['S5','S6','S3','S7'],
            'R3': ['S2','S6'],
            }
    return Subway(routes,stops,stop2routes,route2stops)

def test_subway_get_route():
    subway = create_dummy_subway()
    route = subway.get_route('R1')
    assert (route.name == 'route1')

def test_subway_get_stop():
    subway = create_dummy_subway()
    stop = subway.get_stop('S3')
    assert (stop.name == 'stop3')

def test_subway_get_routes():
    subway = create_dummy_subway()
    routes = subway.get_routeIds('S2')
    trueNames = ['R1','R3']
    assert routes == trueNames

def test_subway_get_stops():
    subway = create_dummy_subway()
    stops = subway.get_stopIds('R2')
    trueNames = ['S5','S6','S3','S7']
    assert stops == trueNames

def test_subway_next_routeIds():
    subway = create_dummy_subway()
    routes = subway.get_next_routeIds('R2')
    trueVal = ['R1','R3']
    assert set(trueVal) == set(routes)

def test_isIn():
    subway = create_dummy_subway()
    route = subway.get_route('R1')
    routes = subway.get_next_routes('R1')
    assert route == Route('R1','route1')
    assert type(routes) == list
    print(routes)
    assert subway.isIn(route,routes) == False

### TESTS PATH FINDER

def test_find_path_same_route():
    subway = create_dummy_subway()
    travel = get_travel(subway,'S1','S4')
    foundRouteIds = [x.id for x in travel.routes]
    assert (set(foundRouteIds) == set(['R1']))

def test_find_path_diff_routes():
    subway = create_dummy_subway()
    travel = get_travel(subway,'S1','S7')
    foundRouteIds = [x.id for x in travel.routes]
    assert (set(foundRouteIds) == set(['R1','R2']))

def test_find_path_diff_routes():
    subway = create_dummy_subway()
    travel = get_travel(subway,'S1','S6')
    foundRouteIds = [x.id for x in travel.routes]
    cond = ( (set(foundRouteIds) == set(['R1','R3'])) or \
             (set(foundRouteIds) == set(['R1','R2'])) )
    assert cond

