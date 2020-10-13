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

from apps.regions.models import Area
from apps.regions.serializers import AreaDetailSerializer

pytestmark = [pytest.mark.django_db, pytest.mark.app_regions, pytest.mark.areas]


def test_get_area_detail(api_client):
    area_pk = 1
    serializer = AreaDetailSerializer(Area.objects.get(pk=area_pk))

    response = api_client.get(f"/areas/{area_pk}/")

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_area_not_found(api_client):
    response = api_client.get(f"/areas/{10000000000}/")

    assert response.status_code == 404
