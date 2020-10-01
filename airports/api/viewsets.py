from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from airports.api.serializers import AirportSerializer
from airports.models import Airport


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    @action(methods=['get'], detail=False)
    def count(self, request):
        return Response({ "ok": "true" })
        pass
