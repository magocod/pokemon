"""
These tests rely on the (load_pokemons) command to get data

call_command("load_pokemons")

Note:

- future versions will adjust these conditions
"""

import pytest

# from apps.pokemons.models import Captured
from apps.pokemons.serializers import SwapPartyMemberSerializer

from .fixtures import fake_pokemon_catch

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.captured_swap_error,
]


def test_change_pokemons_that_dont_exist(api_client_user):
    api_client, user = api_client_user

    # This test depends on this function, care must be taken when modifying
    fake_pokemon_catch(user.id, active=2, storage=2)

    request_data = {
        "entering_the_party": 200000000,
        "leaving_the_party": 400000000,
    }
    serializer = SwapPartyMemberSerializer(data=request_data)

    response = api_client.post("/pokemons/own/swap/", request_data, format="json")

    assert response.status_code == 400
    assert not serializer.is_valid()
    assert (
        response.data["entering_the_party"][0] == "pokemon to exchange does not exist"
    )
    assert response.data["leaving_the_party"][0] == "pokemon to exchange does not exist"


def test_change_pokemons_that_do_not_belong_to_the_user(api_client_user, create_user):
    api_client, user = api_client_user
    other_user = create_user()

    # This test depends on this function, care must be taken when modifying
    query_team, query_storage = fake_pokemon_catch(other_user.id, active=2, storage=2)

    request_data = {
        "entering_the_party": query_storage[0].id,
        "leaving_the_party": query_team[0].id,
    }
    serializer = SwapPartyMemberSerializer(
        data=request_data, context={"user_id": user.id}
    )

    response = api_client.post("/pokemons/own/swap/", request_data, format="json")

    assert response.status_code == 400
    assert not serializer.is_valid()
    assert (
        response.data["entering_the_party"][0] == "this pokemon is not in user storage"
    )
    assert (
        response.data["leaving_the_party"][0] == "this pokemon is not in user storage"
    )
