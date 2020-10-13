"""
These tests rely on the (load_regions, load_pokemons, load_areas)
command to get data

executed strictly in this order
call_command("load_regions")
call_command("load_pokemons")
call_command("load_areas")

Note: future versions will adjust these conditions
"""

import pytest

from apps.regions.models import Location
from apps.regions.serializers import LocationDetailSerializer

pytestmark = [pytest.mark.django_db, pytest.mark.app_regions, pytest.mark.locations]


def test_get_location_detail(api_client):
    location_pk = 1
    serializer = LocationDetailSerializer(Location.objects.get(pk=location_pk))

    response = api_client.get(f"/location/{location_pk}/")

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_region_not_found(api_client):
    response = api_client.get(f"/location/{10000000000}/")

    assert response.status_code == 404
