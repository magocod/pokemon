import random
import string

from apps.pokemons.models import Specie, Captured

def random_name(length = 10):
    """
    ...
    
    Keyword Arguments:
        length {number} -- [description] (default: {10})
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def fake_pokemon_catch(user_id: int, quantity = 3):
    """
    add pokemons captures to a user
    
    Arguments:
        user_id {int} -- [description]
        quantity {int}
    
    Returns:
        [tuple]

    query_team = active pokemon team
    query_storage = pokemon in storage
    """

    Captured.objects.bulk_create(
        Captured(
            nick_name=random_name(),
            is_party_member=True,
            specie_id=random.randint(1,25),
            user_id=user_id
        ) for name in range(quantity)
    )
    query_team = Captured.objects.filter(
        is_party_member=True,
        user_id=user_id
    )

    Captured.objects.bulk_create(
        Captured(
            nick_name=random_name(),
            is_party_member=False,
            specie_id=random.randint(1,25),
            user_id=user_id
        ) for name in range(quantity)
    )
    query_storage = Captured.objects.filter(
        is_party_member=True,
        user_id=user_id
    )

    return query_team, query_storage


def pokemon_team_full_charge(user_id: int):
    """
    
    Arguments:
        user_id {int} -- [description]
    
    Returns:
        [tuple] -- [active pokemon team]
    """
    Captured.objects.bulk_create(
        Captured(
            nick_name=random_name(),
            is_party_member=True,
            specie_id=random.randint(1,25),
            user_id=user_id
        ) for name in range(Captured.active_member_limit())
    )
    query_team = Captured.objects.filter(
        is_party_member=True,
        user_id=user_id
    )
    return query_team
