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
        print('init_users...')
        call_command("init_users")
        
        # should be called in this order
        print('load_regions...')
        call_command("load_regions")
        print('load_pokemons...')
        call_command("load_pokemons")
        print('load_areas...')
        call_command("load_areas")
        print('...finish')
