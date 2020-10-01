import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airports.models import Airport
from flights.api.serializers import FlightSerializer
from flights.models import Flights

from datetime import datetime
from datetime import timedelta

from constants import BASE_URL, API_KEY, API_USER, API_PASS
from utils import get_all_airports_combinations, find_missing_flights, haversine


class FlightViewSet(ModelViewSet):
    queryset = Flights.objects.all()
    serializer_class = FlightSerializer

    @action(methods=['get'], detail=False)
    def seed(self, request):
        all_airports = Airport.objects.all().values_list('iata', flat=True)
        combinations = get_all_airports_combinations(all_airports)
        missing_flights = find_missing_flights(all_airports, combinations)

        for flight in missing_flights:
            arrival = flight['arrival_iata']
            departure = flight['departure_iata']

            target_time = datetime.now() + timedelta(days=40)
            formatted_date = target_time.strftime("%Y-%m-%d")

            url = f"{BASE_URL}/search/{API_KEY}/{departure}/{arrival}/{formatted_date}"
            response = requests.get(url, auth=(API_USER, API_PASS))

            if response.status_code == 401:
                return Response({"error": "Unauthorized"}, 401)

            flight_dict = response.json()

            available_flights = len(flight_dict['options'])

            # Caso não tenha vôos disponíveis
            if available_flights <= 0:
                continue

            # Calcular distância
            summary = flight_dict['summary']
            from_lat = summary['from']['lat']
            from_lon = summary['from']['lon']
            to_lat = summary['to']['lat']
            to_lon = summary['to']['lon']

            distance = haversine(from_lon, from_lat, to_lon, to_lat)

            # Calcular Preços
            prices = [x['fare_price'] for x in flight_dict['options']]
            lowest_price = min(prices)
            price_per_km = lowest_price / distance

            lowest_option = next((item for item in flight_dict['options'] if item['fare_price'] == lowest_price), None)

            # Modelo de avião
            aircraft_model = lowest_option['aircraft']['model']
            aircraft_manufacturer = lowest_option['aircraft']['manufacturer']

            # Calcular Velocidade
            arrival_time = datetime.fromisoformat(lowest_option['arrival_time'])
            departure_time = datetime.fromisoformat(lowest_option['departure_time'])
            flight_duration = (arrival_time - departure_time).total_seconds() / 60  # Tempo em Minutos
            average_speed = distance / (flight_duration / 60)  # Tempo em Horas

            new_flight_attributes = {
                "url": url,
                "lowest_price": lowest_price,
                "distance": distance,
                "aircraft_model": aircraft_model,
                "aircraft_manufacturer": aircraft_manufacturer,
                "price_per_km": price_per_km,
                "departure_iata": departure,
                "arrival_iata": arrival,
                "average_speed": average_speed,
                "flight_duration": flight_duration,
            }

            new_flight = Flights(**new_flight_attributes)
            new_flight.save()

        return Response({"message": "Seeds created"}, 201)
