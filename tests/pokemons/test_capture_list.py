"""
These tests rely on the (load_regions) command to get data

call_command("load_regions")

Note: future versions will adjust these conditions
"""

import pytest

from apps.pokemons.models import Captured
from apps.pokemons.serializers import CapturedSerializer

from .fixtures import fake_pokemon_catch

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.captured_list,
]


def test_get_all_pokemon_from_a_user(api_client_user):
    api_client, user = api_client_user

    # (party_member, pokemom_storage)
    fake_pokemon_catch(user.id)

    serializer = CapturedSerializer(Captured.objects.filter(user_id=user.id), many=True)
    response = api_client.get("/pokemons/own/")

    assert response.status_code == 200
    assert response.data == serializer.data


def test_get_all_active_pokemon_of_a_user(api_client_user):
    api_client, user = api_client_user

    # (party_member, pokemom_storage)
    query_team, _ = fake_pokemon_catch(user.id)

    serializer = CapturedSerializer(
        # Captured.objects.filter(
        #     is_party_member=True,
        #     user_id=user.id
        # ),
        query_team,
        many=True,
    )
    response = api_client.get("/pokemons/own/party/")

    assert response.status_code == 200
    assert response.data == serializer.data
