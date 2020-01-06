from pathFinder import get_travel
from test_mbta import create_dummy_subway

''' available user actions; controls how to display info '''

def sortHubStops(hubStops):

    numRoutes = [len(self.subway.get_routeIds(x)) for x in hubStops]
    _, idxs = [list(x) for x in zip(*sorted(zip(
        numRoutes, range(len(numRoutes)) )))]
    hubStops = [hubStops[i] for i in idxs]

    return hubStops

class Client:

    def __init__(self,subway):
        self.subway = subway

    def print_subway_routes(self):
        routes = self.subway.get_all_routes()
        s = ', '.join([x.name for x in routes])
        print('Subway routes: '+s)

    def print_longest_route(self):
        ''' print route name and count of stops '''
        routes = self.subway.get_all_routes()
        numStops = [len(self.subway.get_stopIds(x)) for x in routes]
        idx = numStops.index(max(numStops))
        maxRoute = routes[idx]
        print('Longest route is {} with {} stops'.format(
            maxRoute.name, numStops[idx]))

    def print_shortest_route(self):
        ''' returns route name and count of stops '''
        routes = self.subway.get_all_routes()
        numStops = [len(self.subway.get_stopIds(x)) for x in routes]
        idx = numStops.index(min(numStops))
        minRoute = routes[idx]
        print('Shortest route is {} with {} stops'.format(
            minRoute.name, numStops[idx]))

    def print_hub_stops(self):
        ''' a hub stop is a stop connecting multiple routes.
            returns hub stops and corresponding route names '''
        stops = self.subway.get_all_stops()
        numRoutes = [len(self.subway.get_routeIds(x)) for x in stops]
        hubStops = [x for i,x in enumerate(stops) if (numRoutes[i] > 1)]
        #hubStops = sortHubStops(hubStops)
        for stop in hubStops:
            s = ', '.join([x.name for x in self.subway.get_routes(stop)])
            print('{:25s}: {}'.format(stop.name, s))

    def print_travel(self, originStop, destinationStop):
        travel = get_travel(self.subway, originStop, destinationStop)
        stop1 = self.subway.get_stop(originStop)
        stop2 = self.subway.get_stop(destinationStop)
        print('From {} to {}: {}'.format(stop1.name, stop2.name, travel.info()))

if __name__ == '__main__':

    # CREATE SUBWAY OBJECT
    subway = create_dummy_subway()
    client = Client(subway)

    print('QUESTION 1:\n')
    client.print_subway_routes()

    print('\nQUESTION 2:\n')
    client.print_longest_route(); print('\n')
    client.print_shortest_route();
    client.print_hub_stops()

    print('\nQUESTION 3:\n')
    originStopName = 'S1'
    destinationStopName = 'S4'
    client.print_travel(originStopName,destinationStopName)

    originStopName = 'S1'
    destinationStopName = 'S7'
    client.print_travel(originStopName,destinationStopName)

    print('\nDONE')
