import json

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    ...
    """

    def handle(self, *args, **options):
        """
        ...
        """
        
        # should be called in this order
        call_command("load_regions")
        call_command("load_pokemons")
        call_command("load_areas")
