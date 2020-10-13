from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    ...
    """

    # def add_arguments(self, parser):
    #     parser.add_argument("-l", "--lazy", type=bool, default=False)

    def handle(self, *args, **options):
        """
        ...
        """
        print("init_users...")
        call_command("init_users")

        # should be called in this order
        print("load_regions...")
        call_command("load_regions")
        print("load_pokemons...")
        call_command("load_pokemons")
        print("load_areas...")
        call_command("load_areas")
        print("...finish")
