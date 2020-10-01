from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airports.api.serializers import AirportSerializer
from airports.models import Airport
from constants import API_KEY, API_PASS, API_USER, BASE_URL

import requests

from flights.models import Flights


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    @action(methods=['post'], detail=False)
    def seed(self, request):
        response = requests.get(f"{BASE_URL}/airports/{API_KEY}", auth=(API_USER, API_PASS))

        if response.status_code == 401:
            return Response({"error": "Unauthorized"}, 401)

        airports_dict = response.json()
        for key, airport in airports_dict.items():
            if Airport.find_airport(key):
                continue

            new_airport = Airport(**airport)
            new_airport.save()

        return Response({"message": "Seeds created"}, 201)

    @action(methods=['get'], detail=False)
    def count(self, request):
        airports = Airport.objects.values('city').annotate(airports=Count('city')).order_by('-airports')[:1]
        return Response(airports, 200)

    @action(methods=['get'], detail=False)
    def distance(self, request):
        airports = Airport.objects.all().values_list('iata')
        return_arr = []
        for iata, in airports:
            highest = Flights.find_flight_distance_order(iata, '-')
            lowest = Flights.find_flight_distance_order(iata)

            highest_iata = len(highest) > 0 and highest[0]['arrival_iata'] or 'Não há vôo disponível'
            lowest_iata = len(lowest) > 0 and lowest[0]['arrival_iata'] or 'Não há vôo disponível'

            return_arr.append({
                "from": iata,
                "highest_duration": highest_iata,
                "lowest_duration": lowest_iata,
            })

        return Response(return_arr, 200)
