import json

import pytest

from django.conf import settings

from apps.pokemons.models import Specie
from apps.regions.models import Area, Location, Region

pytestmark = [pytest.mark.django_db, pytest.mark.database]


def test_database_connection():
    """
    The command (init_database) is called when the database starts
    """

    with open(settings.BASE_DIR / "data/areas.json") as json_file:
        total_expected = len(json.load(json_file)["data"])
        # print(Area.objects.count())
        assert total_expected == Area.objects.count()

    with open(settings.BASE_DIR / "data/locations.json") as json_file:
        total_expected = len(json.load(json_file)["data"])
        # print(Location.objects.count())
        assert total_expected == Location.objects.count()

    with open(settings.BASE_DIR / "data/pokemons.json") as json_file:
        total_expected = len(json.load(json_file)["data"])
        # print(Specie.objects.count())
        assert total_expected == Specie.objects.count()

    with open(settings.BASE_DIR / "data/regions.json") as json_file:
        total_expected = len(json.load(json_file)["data"])
        # print(Region.objects.count())
        assert total_expected == Region.objects.count()
