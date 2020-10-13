"""
These tests rely on the (load_pokemons) command to get data

call_command("load_pokemons")

Note:

- future versions will adjust these conditions
- this test is misdirected, very complex to evaluate
- It is possible that the same executor of this test
after a while does not understand it
"""

import pytest

from apps.pokemons.models import Captured
from apps.pokemons.serializers import CapturedSerializer
from apps.pokemons.exceptions import ACTIVE_POKEMON_LIMIT_REACHED

from .fixtures import fake_pokemon_catch

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.captured_swap,
]

ERROR_CODES = [400, 403, 500]

SWAP_CASES = [
    # remove an active pokemon from the team and add one from storage
    # with full pokemon team
    (
        # case
        {
            # pokemons pm = is_party_member
            "pokemon_team": 6, # pm -> true -> id: 1 - 6
            "pokemon_storage": 3, # pm -> false -> id: 7 - 9
            # request
            "request": {
                "entering_the_party": 7,
                "leaving_the_party": 5,
            }
        },
        # expected
        {
            "status_code": 200,
            "pokemon_team": 6,
            "pokemon_storage": 3,
            # determine if after consultation the Pokémon in the team or
            # warehouse are expected to change
            "teams_change": True
        }
    ),
    # add pokemon from storage to active team
    # has team space
    (
        # case
        {
            # pokemons pm = is_party_member
            "pokemon_team": 2, # pm -> true -> id: 1 - 2
            "pokemon_storage": 3, # pm -> false -> id: 3 - 5
            # request
            "request": {
                "entering_the_party": 4, #
                "leaving_the_party": None,
            }
        },
        # expected
        {
            "status_code": 200,
            "pokemon_team": 3,
            "pokemon_storage": 2,
            # determine if after consultation the Pokémon in the team or
            # warehouse are expected to change
            "teams_change": True
        }
    ),
    # move pokemon from active team to storage
    (
        # case
        {
            # pokemons pm = is_party_member
            "pokemon_team": 4, # pm -> true -> id: 1 - 4
            "pokemon_storage": 2, # pm -> false -> id: 5 - 6
            # request
            "request": {
                "entering_the_party": None,
                "leaving_the_party": 2,
            }
        },
        # expected
        {
            "status_code": 200,
            "pokemon_team": 3,
            "pokemon_storage": 3,
            # determine if after consultation the Pokémon in the team or
            # warehouse are expected to change
            "teams_change": True
        }
    ),
    # move active pokemon to active pokemon
    # move pokemon from storage to storage
    (
        # case
        {
            # pokemons pm = is_party_member
            "pokemon_team": 3, # pm -> true -> id: 1 - 3
            "pokemon_storage": 3, # pm -> false -> id: 4 - 6
            # request
            "request": {
                "entering_the_party": 1,
                "leaving_the_party": 4,
            }
        },
        # expected
        {
            "status_code": 200,
            "pokemon_team": 3,
            "pokemon_storage": 3,
            # determine if after consultation the Pokémon in the team or
            # warehouse are expected to change
            "teams_change": False
        }
    ),
    # add pokemon on active team, without having space
    # (does not remove one from team first)
    (
        # case
        {
            # pokemons pm = is_party_member
            "pokemon_team": 6, # pm -> true -> id: 1 - 6
            "pokemon_storage": 2, # pm -> false -> id: 7 - 8
            # request
            "request": {
                "entering_the_party": 8,
                "leaving_the_party": None,
            }
        },
        # expected
        {
            "status_code": 403,
            "pokemon_team": 6,
            "pokemon_storage": 2,
            # determine if after consultation the Pokémon in the team or
            # warehouse are expected to change
            "teams_change": False
        }
    )
]


@pytest.mark.parametrize("case, expected", SWAP_CASES)
def test_swap_team_pokemon_and_warehouse(case, expected, api_client_user):
    api_client, user = api_client_user

    # This test depends on this function, care must be taken when modifying
    query_team, query_storage = fake_pokemon_catch(
        user.id,
        active=case["pokemon_team"],
        storage=case["pokemon_storage"]
    )

    # force query evaluation
    origin_team_id = list(query_team.values_list('id', flat=True))
    origin_storage_id = list(query_storage.values_list('id', flat=True))

    response = api_client.post("/pokemons/own/swap/", case["request"], format="json")

    assert response.status_code == expected["status_code"]

    current_team = Captured.objects.filter(
        is_party_member=True,
        user_id=user.id
    )
    current_storage = Captured.objects.filter(
        is_party_member=False,
        user_id=user.id
    )

    if not expected["status_code"] in ERROR_CODES:
        # check active pokemon team
        current_team = Captured.objects.filter(
            is_party_member=True,
            user_id=user.id
        )
        serializer = CapturedSerializer(
            current_team,
            many=True
        )
        assert response.data == serializer.data
    else:
        # if the result is an error check error
        if response.status_code == 403:
            assert response.data["detail"] == ACTIVE_POKEMON_LIMIT_REACHED
        else:
            # other exceptions are not currently handled
            raise Exception("exceptions are not currently handled")

    # why check the id, to check if the team changed
    # print("origin team", origin_team_id)
    # print("current_team", current_team.values_list("id", flat=True))

    # print("origin_storage", origin_storage_id)
    # print("current_storage", current_storage.values_list("id", flat=True))

    # using the identification it is verified if I change a place element
    # lazy and not very accurate check
    current_team_id = set(current_team.values_list("id", flat=True))
    current_storage_id = set(current_storage.values_list("id", flat=True))

    if expected["teams_change"]:
        assert set(origin_team_id) != current_team_id
        assert set(origin_storage_id) != current_storage_id
    else:
        assert set(origin_team_id) == current_team_id
        assert set(origin_storage_id) == current_storage_id

    # because check the query make sure the database has records
    assert expected["pokemon_team"] == current_team.count()
    assert expected["pokemon_storage"] == current_storage.count()
