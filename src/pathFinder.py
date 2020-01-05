from traveling import Travel, TravelCandidates
from dataStructures import Stop,Route

MAX_TRAVEL_CANDIDATES = 100

def get_travel(originStopName,destinationStopName):
    '''
    Examples:
        1. Davis to Kendall -> Redline
        2. Ashmont to Arlington -> Redline, Greenline
    '''

    originStop = Stop.get(originStopName)
    destinationStop = Stop.get(destinationStopName)

    originRoutes = originStop.routes
    destinationRoutes = destinationStop.routes

    travelCandidates = TravelCandidates()

    initTravels = [Travel([x]) for x in originRoutes]
    for initTravel in initTravels: travelCandidates.add(initTravel)

    while not(travelCandidates.isEmpty()):

        travel = travelCandidates.pop()

        if travel.reaches(destinationRoutes): return travel

        travelCandidates.extend(travel) # add more candidates

        if travelCandidates.num_travels > MAX_TRAVEL_CANDIDATES:
            raise ValueError('Too many travel candidates')

    print('Destination: {} cannot be reached from Origin: {}')

    return Travel()

    return travel

