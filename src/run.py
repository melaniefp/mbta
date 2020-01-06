from dataRetriever import DataRetriever
from client import Client

from test_mbta import create_dummy_subway

if __name__ == '__main__':

    # CREATE SUBWAY OBJECT
    #subway = create_dummy_subway()

    print('\nLoading data...\n')
    dr = DataRetriever()
    subway = dr.get_subway()


    client = Client(subway)

    print('QUESTION 1:\n')
    client.print_subway_routes()

    print('\nQUESTION 2:\n')
    client.print_longest_route(); print('\n')
    client.print_shortest_route();
    client.print_hub_stops()

    print('\nQUESTION 3:\n')
    origin = 'place-davis' # 'Davis'
    destination = 'place-knncl' # 'Kendall/MIT'
    client.print_travel(origin,destination)

    origin = 'place-asmnl' #'Ashmont'
    destination = 'place-armnl' #'Arlington'
    client.print_travel(origin,destination)

    print('\nDONE')
