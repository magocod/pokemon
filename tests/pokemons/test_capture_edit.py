"""
These tests rely on the (load_regions) command to get data

call_command("load_regions")

Note: future versions will adjust these conditions
"""

import random

import pytest

from apps.pokemons.models import Captured
from apps.pokemons.serializers import CapturedBasicSerializer, CapturedEditSerializer

from .fixtures import fake_pokemon_catch, random_name

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.captured_edit,
]


# parameterize tests, delayed by time
# put and patch routes share code


request_data = {
    "nick_name": random_name(),
}


def test_edit_the_name_of_the_captured_pokemon(api_client_user):
    api_client, user = api_client_user

    captured = Captured.objects.create(
        nick_name=random_name(),
        is_party_member=True,
        specie_id=random.randint(1, 25),
        user_id=user.id,
    )
    captured_id = captured.id
    old_nick_name = captured.nick_name

    response = api_client.put(
        f"/pokemons/own/{captured_id}/", request_data, format="json"
    )

    captured = Captured.objects.get(id=captured_id)
    serializer = CapturedBasicSerializer(captured)

    assert response.status_code == 200

    assert response.data == serializer.data
    assert old_nick_name != captured.nick_name


def test_validate_form_change_nickname_of_captured_pokemon(api_client_user):
    api_client, user = api_client_user

    captured = Captured.objects.create(
        nick_name=random_name(),
        is_party_member=True,
        specie_id=random.randint(1, 25),
        user_id=user.id,
    )
    captured_id = captured.id
    old_nick_name = captured.nick_name

    invalid_request_data = {
        "nick_name": False,
    }
    serializer = CapturedEditSerializer(data=invalid_request_data)
    response = api_client.put(
        f"/pokemons/own/{captured_id}/", invalid_request_data, format="json"
    )

    captured = Captured.objects.get(id=captured_id)

    assert response.status_code == 400

    assert not serializer.is_valid()
    assert "nick_name" in response.data
    assert old_nick_name == captured.nick_name


def test_prohibit_editing_the_nickname_of_pokemon_if_it_is_not_the_user(
    api_client_user, create_user
):
    api_client, user = api_client_user

    other_user = create_user()

    captured = Captured.objects.create(
        nick_name=random_name(),
        is_party_member=True,
        specie_id=random.randint(1, 25),
        user_id=other_user.id,
    )
    nick_name = captured.nick_name

    response = api_client.put(
        f"/pokemons/own/{captured.id}/", request_data, format="json"
    )

    captured = Captured.objects.get(id=captured.id)

    assert response.status_code == 403
    # assert response.data ==
    assert nick_name == captured.nick_name


def test_pokemon_not_found_to_edit_nickname(api_user):
    response = api_user.put(
        f"/pokemons/own/{10000000000}/", request_data, format="json"
    )

    assert response.status_code == 404


def test_release_pokemon(api_client_user):
    api_client, user = api_client_user
    query_team, _ = fake_pokemon_catch(user.id, 1)
    captured_id = query_team[0].id

    user_pokemons_count = Captured.objects.filter(user_id=user.id).count()

    response = api_client.delete(f"/pokemons/own/{captured_id}/")

    assert response.status_code == 204
    assert user_pokemons_count - 1 == Captured.objects.filter(user_id=user.id).count()


def test_pokemon_not_found_to_release(api_client_user):
    api_client, user = api_client_user

    fake_pokemon_catch(user.id, 1)
    user_pokemons_count = Captured.objects.filter(user_id=user.id).count()

    response = api_client.delete(f"/pokemons/own/{1000000000000000}/")

    assert response.status_code == 404
    assert user_pokemons_count == Captured.objects.filter(user_id=user.id).count()


def test_forbidden_to_release_pokemon_other_than_the_user(api_client_user, create_user):
    api_client, user = api_client_user

    other_user = create_user()
    captured = Captured.objects.create(
        nick_name=random_name(),
        is_party_member=True,
        specie_id=random.randint(1, 25),
        user_id=other_user.id,
    )
    pokemons_count = Captured.objects.filter(user_id=other_user.id).count()

    response = api_client.delete(f"/pokemons/own/{captured.id}/")

    assert response.status_code == 403
    assert pokemons_count == Captured.objects.filter(user_id=other_user.id).count()
