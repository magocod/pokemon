from rest_framework.exceptions import PermissionDenied
from .models import Captured


LIMIT_POKEMON = Captured.active_member_limit()

POKEMON_IS_NOT_THE_USER = "this pokemon is not in user storage"
ACTIVE_POKEMON_LIMIT_REACHED = f"you can only have {LIMIT_POKEMON} pokemon in your team"


class PokemonIsNotTheUser(PermissionDenied):
    """
    Extends:
        PermissionDenied

    Variables:
        default_detail {str} -- [description]
    """

    default_detail = POKEMON_IS_NOT_THE_USER


class ActivePokemonLimitReached(PermissionDenied):
    """
    Extends:
        PermissionDenied

    Variables:
        default_detail {str} -- [description]
    """

    default_detail = ACTIVE_POKEMON_LIMIT_REACHED
