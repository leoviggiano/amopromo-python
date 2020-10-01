from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airports.api.serializers import AirportSerializer
from airports.models import Airport
from constants import API_KEY, API_PASS, API_USER, BASE_URL

import json, requests


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
        pass

    @action(methods=['get'], detail=False)
    def count(self, request):
        queryset = Airport.objects.all()
        return Response({ "ok": "true" })
        pass
