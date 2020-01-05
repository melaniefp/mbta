from dataStructures import Stop,Route
from pathFinder import get_travel
import ipdb

''' available user actions; controls how to display info '''

def print_subway_routes():
    routes = Route.get_subway_routes()
    s = ', '.join([x.name for x in routes])
    print('Subway routes: '+s)

def print_longest_route():
    ''' print route name and count of stops '''
    routes = Route.get_subway_routes()
    numStops = [x.num_stops for x in routes]
    maxRoute = routes[ numStops.index(max(numStops)) ]
    print('Longest route is {} with {} stops'.format(
        maxRoute.name,maxRoute.num_stops))

def print_shortest_route():
    ''' returns route name and count of stops '''
    routes = Route.get_subway_routes()
    numStops = [x.num_stops for x in routes]
    minRoute = routes[ numStops.index(min(numStops)) ]
    print('Shortest route is {} with {} stops'.format(
        minRoute.name,minRoute.num_stops))
    return

def print_hub_stops():
    ''' a hub stop is a stop connecting multiple routes.
        returns hub stops and corresponding route names '''
    stops = Stop.get_subway_stops()
    hubStops = [x for x in stops if (x.num_routes > 1)]
    numRoutes = [x.num_routes for x in hubStops]
    _, idxs = [list(x) for x in zip(*sorted(zip(
        numRoutes, range(len(numRoutes)) )))]
    hubStops = [hubStops[i] for i in idxs]

    for stop in hubStops: print_stop(stop)
    return

# TODO: cleaner to move to Stop class
def print_stop(stop):
    s = ', '.join([x.name for x in stop.routes])
    print('{:25s}: {}'.format(stop.name, s))

def print_travel(originStop, destinationStop):
    travel = get_travel(originStop, destinationStop)
    print('From {} to {}: {}'.format(originStop, destinationStop, travel.info()))

if __name__ == '__main__':

    print('QUESTION 1:\n')
    print_subway_routes()

    print('\nQUESTION 2:\n')
    print_longest_route(); print('\n')
    print_shortest_route();
    print_hub_stops()

    print('\nQUESTION 3:\n')
    originStopName = 'Davis'
    destinationStopName = 'Kendall/MIT'
    print_travel(originStopName,destinationStopName)

    originStopName = 'Ashmont'
    destinationStopName = 'Arlington'
    print_travel(originStopName,destinationStopName)

    print('\nDONE')
