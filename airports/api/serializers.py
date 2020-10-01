from rest_framework.serializers import ModelSerializer
from airports.models import Airport


class AirportSerializer(ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"
