from rest_framework.viewsets import ModelViewSet

from flights.api.serializers import FlightSerializer
from flights.models import Flights


class FlightViewSet(ModelViewSet):
    queryset = Flights.objects.all()
    serializer_class = FlightSerializer
