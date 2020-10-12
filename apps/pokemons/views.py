from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from .models import Specie
from .serializers import SpecieSerializer


class SpecieDetail(APIView):
    """
    Retrieve, specie instance.
    """

    def get_object(self, pk):
        try:
            return Specie.objects.get(pk=pk)
        except Specie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        specie = self.get_object(pk)
        serializer = SpecieSerializer(specie)
        return Response(serializer.data)
