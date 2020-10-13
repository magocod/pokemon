# from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from .models import Area, Location, Region
from .serializers import (
    AreaDetailSerializer,
    LocationDetailSerializer,
    RegionDetailSerializer,
    RegionSerializer,
)

# second time here, if there is a possibility
# to switch to generic views


class RegionList(APIView):
    """
    List all regions
    """

    def get(self, request, format=None):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


class RegionDetail(APIView):
    """
    Retrieve, region instance.
    """

    def get_object(self, pk):
        try:
            return Region.objects.get(pk=pk)
        except Region.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        region = self.get_object(pk)
        serializer = RegionDetailSerializer(region)
        return Response(serializer.data)


class LocationDetail(APIView):
    """
    Retrieve, location instance.
    """

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationDetailSerializer(location)
        return Response(serializer.data)


class AreaDetail(APIView):
    """
    Retrieve, area instance.
    """

    def get_object(self, pk):
        try:
            return Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        area = self.get_object(pk)
        serializer = AreaDetailSerializer(area)
        return Response(serializer.data)
