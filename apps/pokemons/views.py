from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from .exceptions import PokemonIsNotTheUser
from .models import Captured, Specie
from .serializers import (
    CapturedCreateSerializer,
    CapturedEditSerializer,
    CapturedSerializer,
    SpecieSerializer,
    SwapPartyMemberSerializer,
)

# second time here, if there is a possibility
# to switch to generic views


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


class CapturedList(APIView):
    """
    - List all user pokemons (all)
    - create (max 6 active)
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Captured.objects.filter(user_id=request.user.id)
        serializer = CapturedSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CapturedCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            captured_serialized = serializer.save()
            return Response(captured_serialized, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CapturedDetail(APIView):
    """
    - update (only nick_name)
    - delete

    Note: instance -> Captured model
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, user_id):
        try:
            instance = Captured.objects.get(pk=pk)
        except Captured.DoesNotExist:
            raise Http404

        if instance.user_id != user_id:
            raise PokemonIsNotTheUser

        return instance

    def put(self, request, pk, format=None):
        instance = self.get_object(pk, request.user.id)
        serializer = CapturedEditSerializer(instance, data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        repeated code
        """
        instance = self.get_object(pk, request.user.id)
        serializer = CapturedEditSerializer(instance, data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk, request.user.id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CapturedParty(APIView):
    """
    List all user pokemons party
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Captured.objects.filter(
            is_party_member=True, user_id=request.user.id
        )
        serializer = CapturedSerializer(queryset, many=True)
        return Response(serializer.data)


class SwapPartyMember(APIView):
    """
    trade, add, or remove a user's active Pokémon
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SwapPartyMemberSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
