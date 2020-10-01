from rest_framework.serializers import ModelSerializer
from flights.models import Flights


class FlightSerializer(ModelSerializer):
    class Meta:
        model = Flights
        fields = "__all__"
