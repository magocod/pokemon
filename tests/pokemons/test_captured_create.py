"""
These tests rely on the (load_pokemons) command to get data

call_command("load_pokemons")

Note: future versions will adjust these conditions
"""

import pytest

from apps.pokemons.models import Captured
from apps.pokemons.serializers import CapturedBasicSerializer, CapturedCreateSerializer

from .fixtures import pokemon_team_full_charge, random_name

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.captured_create,
]


def test_capture_pokemon_with_team_space(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 1,
        "nick_name": random_name(),
        "is_party_member": True,
    }
    response = api_client.post("/pokemons/own/", request_data, format="json")

    assert response.status_code == 201

    serializer = CapturedBasicSerializer(
        Captured.objects.get(id=response.data["id"]),
    )

    assert response.data == serializer.data


def test_capture_pokemon_send_to_warehouse_with_space_on_team(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 1,
        "nick_name": random_name(),
        "is_party_member": False,
    }
    response = api_client.post("/pokemons/own/", request_data, format="json")

    assert response.status_code == 201

    captured = Captured.objects.get(id=response.data["id"])
    serializer = CapturedBasicSerializer(captured)

    assert response.data == serializer.data
    assert not captured.is_party_member


def test_catch_pokemon_and_send_it_to_warehouse_because_user_has_full_gear(
    api_client_user,
):
    api_client, user = api_client_user

    request_data = {
        "specie": 5,
        "nick_name": random_name(),
        "is_party_member": True,
    }

    pokemon_team_full_charge(user.id)

    pokemons_count = Captured.objects.filter(user_id=user.id).count()
    pokemons_active_count = Captured.objects.filter(
        is_party_member=True, user_id=user.id
    ).count()

    response = api_client.post("/pokemons/own/", request_data, format="json")

    assert response.status_code == 201

    captured = Captured.objects.get(id=response.data["id"])
    serializer = CapturedBasicSerializer(captured)

    assert response.data == serializer.data
    assert not captured.is_party_member

    assert pokemons_count + 1 == Captured.objects.filter(user_id=user.id).count()
    assert (
        pokemons_active_count
        == Captured.objects.filter(is_party_member=True, user_id=user.id).count()
    )


def test_validate_form_to_capture_pokemon(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": "hello",
        "nick_name": True,
        "is_party_member": 3000,
    }
    serializer = CapturedCreateSerializer(data=request_data)

    captured_count = Captured.objects.count()
    response = api_client.post("/pokemons/own/", request_data, format="json")

    assert response.status_code == 400

    assert not serializer.is_valid()
    assert response.data["specie"] == serializer.errors["specie"]
    assert response.data["nick_name"] == serializer.errors["nick_name"]
    assert response.data["is_party_member"] == serializer.errors["is_party_member"]

    assert captured_count == Captured.objects.count()


def test_validate_pokemon_to_capture_exists(api_client_user):
    api_client, user = api_client_user

    request_data = {
        "specie": 20000000,
        "nick_name": random_name(),
        "is_party_member": True,
    }
    serializer = CapturedCreateSerializer(data=request_data)

    captured_count = Captured.objects.count()
    response = api_client.post("/pokemons/own/", request_data, format="json")

    assert response.status_code == 400

    assert not serializer.is_valid()
    assert response.data["specie"] == serializer.errors["specie"]

    assert captured_count == Captured.objects.count()
