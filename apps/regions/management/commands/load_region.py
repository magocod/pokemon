import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.regions.models import Region, Location


class Command(BaseCommand):
    """
    ...
    """

    @transaction.atomic
    def handle(self, *args, **options):
        """
        ...
        """
        
        # print(settings.BASE_DIR / "data/areas.json")
        with open(settings.BASE_DIR / "data/regions.json") as json_file:
            data_regions = json.load(json_file)['data']

        query_regions = Region.objects.bulk_create([
            Region(
                name=region["name"]
            )
            for region in data_regions
        ])
         

        total_locations: int = 0 # json_file
        # discarded for now, avoid consuming more resources
        # instances_to_save: int = 0

        with open(settings.BASE_DIR / "data/locations.json") as json_file:
            data_locations = json.load(json_file)['data']
            total_locations = len(data_locations)

        for region in query_regions:
            region_locations = [
                Location(
                    name=location["name"],
                    region_id=region.id
                )
                for location in data_locations
                if location["region"] == region.name
            ]

            # instances_to_save = len(region_locations)
            Location.objects.bulk_create(region_locations)

        # show warning in case of saving more or missing items
        # location_exact_amount = total_locations == Location.objects.count()
        # if not location_exact_amount: 
        #     print('location_exact_amount', location_exact_amount)
