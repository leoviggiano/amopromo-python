from math import radians, cos, sin, asin, sqrt
from constants import LIMIT_DATA
from flights.models import Flights


def get_all_airports_combinations(airports: [dict]) -> [dict]:
    all_combinations = {}
    """
        Basicamente a array de aeroportos irá ser iterada, setando a IATA como chave do dicionário,
        E seu valor sendo a array copiada do earoporto removendo a sua própria IATA, pois não há como
        o destino e partida serem iguais
    """
    for key in airports[:LIMIT_DATA]:
        combinations = list(airports[:LIMIT_DATA])
        combinations.remove(key)
        all_combinations[key] = combinations

    return all_combinations


def find_missing_flights(airports: [str], combination_airports: {str: [dict]}) -> [dict]:
    missing_flights = []

    for iata in combination_airports:
        combinations = combination_airports[iata]
        for departure_iata in combinations:
            if not Flights.find_flight(iata, departure_iata):
                missing_flights.append({'arrival_iata': iata, 'departure_iata': departure_iata})

    return missing_flights


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
