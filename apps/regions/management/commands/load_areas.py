import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.regions.models import Area, Location
from apps.pokemons.models import Pokemon


class Command(BaseCommand):
    """
    ...
    """

    @transaction.atomic
    def handle(self, *args, **options):
        """
        ...
        """

        # pending for now, optimize pokemons search to assign
        # based on a naive approach:
        # - many trips to the database
        # - loading all locations in memory

        with open(settings.BASE_DIR / "data/areas.json") as json_file:
            data_areas = json.load(json_file)['data']

        query_locations = Location.objects.all()
        query_pokemons = Pokemon.objects.all()

        # Area.objects.bulk_create([
        #     Area(
        #         name=area["name"],
        #         location_id=query_locations.get(name=area["location"]).id
        #     )
        #     for area in data_areas
        # ])
        # query_areas = Area.objects.all()
        
        for area_data in data_areas:
            area = Area.objects.create(
                name=area_data["name"],
                location_id=query_locations.get(name__iexact=area_data["location"]).id
            )

            pokemons = []

            for name in area_data["pokemons"]:
                try:
                    pokemons.append(query_pokemons.get(name__iexact=name))
                except ObjectDoesNotExist:
                    # warning that pokemon cannot be saved
                    print(f"warning that pokemon {name} cannot be saved")

            # print(pokemons)
            area.pokemons.add(*pokemons)
