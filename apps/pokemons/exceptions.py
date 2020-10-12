from rest_framework.exceptions import PermissionDenied


class PokemonIsNotTheUser(PermissionDenied):
    """
    Extends:
        PermissionDenied
    
    Variables:
        default_detail {str} -- [description]
    """
    default_detail = "this pokemon is not in user storage"
