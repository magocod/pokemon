from rest_framework import serializers

from apps.regions.models import (
    Region,
    Location,
    Area
)
from apps.pokemons.serializers import SpecieBasicSerializer


class AreaSerializer(serializers.ModelSerializer):

    pokemon_count = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ['id', 'name', 'location', 'pokemon_count']

    def get_pokemon_count(self, obj):
        """[summary]

        Arguments:
            obj {Area} -- [description]

        Returns:
            [int] -- [description]
        """
        return obj.pokemons.count()


class AreaDetailSerializer(AreaSerializer):

    pokemons = SpecieBasicSerializer(many=True)
    
    class Meta:
        model = Area
        fields = ['id', 'name', 'location', 'pokemon_count', 'pokemons']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'name']


class LocationDetailSerializer(serializers.ModelSerializer):

    areas = AreaSerializer(many=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'region', 'areas']


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'name']


class RegionDetailSerializer(RegionSerializer):

    locations = LocationSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'locations']
