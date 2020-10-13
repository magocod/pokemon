"""
These tests rely on the (load_regions) command to get data

call_command("load_regions")

Note: future versions will adjust these conditions
"""

import pytest

from apps.pokemons.models import Captured
from apps.pokemons.serializers import CapturedBasicSerializer

from .fixtures import fake_pokemon_catch, pokemon_team_full_charge


pytestmark = [
	pytest.mark.django_db,
	pytest.mark.app_pokemons,
	pytest.mark.captured,
	pytest.mark.captured_create
]


def test_capture_pokemon_with_team_space(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 1,
        "nick_name": "Pedro",
        "is_party_member": True,
    }
    response = api_client.post("/pokemons/own/", request_data, format='json')

    assert response.status_code == 201

    serializer = CapturedBasicSerializer(
        Captured.objects.get(id=response.data["id"]),
    )

    assert response.data == serializer.data


def test_capture_pokemon_send_to_warehouse_with_space_on_team(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 1,
        "nick_name": "Pedro",
        "is_party_member": False,
    }
    response = api_client.post("/pokemons/own/", request_data, format='json')

    assert response.status_code == 201

    captured = Captured.objects.get(id=response.data["id"])
    serializer = CapturedBasicSerializer(captured)

    assert response.data == serializer.data
    assert captured.is_party_member == False


def test_validate_form_to_capture_pokemon(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": "hello",
        "nick_name": True,
        "is_party_member": 3000,
    }
    serializer = CapturedBasicSerializer(data=request_data)

    captured_count = Captured.objects.count()
    response = api_client.post("/pokemons/own/", request_data, format='json')


    assert response.status_code == 400

    assert not serializer.is_valid()
    assert "specie" in response.data
    assert "nick_name" in response.data
    assert "is_party_member" in response.data

    assert captured_count == Captured.objects.count()


def test_validate_pokemon_to_capture_exists(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 20000000,
        "nick_name": "hellou",
        "is_party_member": True,
    }
    serializer = CapturedBasicSerializer(data=request_data)

    captured_count = Captured.objects.count()
    response = api_client.post("/pokemons/own/", request_data, format='json')

    assert response.status_code == 400

    assert not serializer.is_valid()
    assert "specie" in response.data

    assert captured_count == Captured.objects.count()
