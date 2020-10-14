"""
It was only set to test the successful connection in the database,
while no tests were created, delete later
"""

import random
from unittest import mock

import pytest

from apps.pokemons.models import NameStatistic, Specie, Statistic

from .fixtures import random_name

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.app_pokemons,
    pytest.mark.captured,
    pytest.mark.catch_rate,
]


def false_percentage(cls, *args, **kwargs):
    """

    always capture

    Arguments:
        *args {[type]} -- [description]
        **kwargs {[type]} -- [description]

    Returns:
        number -- [description]
    """
    return 100


def fake_pokemon():
    specie, _ = Specie.objects.get_or_create(
        name=random_name(),
        capture_rate=random.randint(45, 80),
        color="green",
        flavor_text="dsds",
        height=10,
        weight=10,
    )
    name, _ = NameStatistic.objects.get_or_create(name="hp")
    Statistic.objects.get_or_create(
        specie_id=specie.id,
        name_id=name.id,
        value=random.randint(25, 80),
    )
    return specie


def test_get_percentage_of_catching_a_pokemon():
    """
    ...
    """

    # pokemon = fake_pokemon()
    # print(pokemon, pokemon.catch_percentage())

    with mock.patch.object(Specie, "catch_percentage", new=false_percentage):
        pokemon = fake_pokemon()
        assert 100 == pokemon.catch_percentage()
