"""
These tests rely on the (load_pokemons)
command to get data

call_command("load_pokemons")

Note: future versions will adjust these conditions
"""

import pytest

from apps.pokemons.models import Specie
from apps.pokemons.serializers import SpecieSerializer


pytestmark = [pytest.mark.django_db, pytest.mark.app_pokemons, pytest.mark.species]


def test_get_specie_detail(api_client):
    specie_id = 1
    serializer = SpecieSerializer(Specie.objects.get(pk=specie_id))

    response = api_client.get(f"/pokemons/{specie_id}/")

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_specie_not_found(api_client):
    response = api_client.get(f"/pokemons/{10000000000}/")

    assert response.status_code == 404
