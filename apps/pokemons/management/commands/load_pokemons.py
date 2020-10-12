import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.pokemons.models import (
    Ability,
    Move,
    Specie,
    Sprite,
    Statistic,
    Type,
    NameStatistic,
)

# import typing


# class PokemonType(typing.TypedDict):
#     """
#     Just as an observation, the actual implementation
#     would not be like this.
#     """
#     capture_rate: int
#     color: str
#     flavor_text: str
#     height: str
#     name: str
#     weight: str
#     # relations
#     abilities: list[str]
#     moves: list[str]
#     sprites: list[str]
#     types: list[str]
#     stats: list[dict[str, typing.Any]]


class Command(BaseCommand):
    """
    ...
    """

    @transaction.atomic
    def handle(self, *args, **options):
        """
        ...
        """

        with open(settings.BASE_DIR / "data/pokemons.json") as json_file:
            data_pokemons = json.load(json_file)["data"]

        # search pokemons metadata
        pokemon_abilities = set()
        pokemon_moves = set()
        pokemon_types = set()
        pokemon_stats = set()

        for pokemon in data_pokemons:
            pokemon_abilities.update(pokemon["abilities"])
            pokemon_moves.update(pokemon["moves"])
            pokemon_types.update(pokemon["types"])
            # the latter consumes more resources,
            # requires prior processing of the property
            pokemon_stats.update([status["name"] for status in pokemon["stats"]])

        # save meta data pokemons
        # note: depending on bd the id is not retrieved

        Ability.objects.bulk_create(
            Ability(name=name) for name in tuple(pokemon_abilities)
        )
        query_abilities = Ability.objects.all()

        Move.objects.bulk_create(Move(name=name) for name in tuple(pokemon_moves))
        query_moves = Move.objects.all()

        Type.objects.bulk_create(Move(name=name) for name in tuple(pokemon_types))
        query_types = Type.objects.all()

        NameStatistic.objects.bulk_create(
            Move(name=name) for name in tuple(pokemon_stats)
        )
        query_statistic = NameStatistic.objects.all()

        # fix later, so many trips to the bd
        for pokemon_data in data_pokemons:

            # print(pokemon_data["name"])
            # utf error in mysql / mariadb
            # print(pokemon_data["name"].encode('utf-8'))
            # print(pokemon_data["flavor_text"].encode('utf-8'))

            pokemon = Specie.objects.create(
                name=pokemon_data["name"],
                capture_rate=pokemon_data["capture_rate"],
                color=pokemon_data["color"],
                flavor_text=pokemon_data["flavor_text"],
                height=pokemon_data["height"],
                weight=pokemon_data["weight"],
            )

            # many to many relations

            pokemon.abilities.add(
                *[
                    obj for obj in query_abilities
                    if obj.name in pokemon_data["abilities"]
                ]
            )

            pokemon.moves.add(
                *[obj for obj in query_moves if obj.name in pokemon_data["moves"]]
            )

            pokemon.types.add(
                *[obj for obj in query_types if obj.name in pokemon_data["types"]]
            )

            # relations

            Sprite.objects.create(
                specie_id=pokemon.id,
                back_default=pokemon_data["sprites"]["back_default"],
                back_female=pokemon_data["sprites"]["back_female"],
                back_shiny=pokemon_data["sprites"]["back_shiny"],
                back_shiny_female=pokemon_data["sprites"]["back_shiny_female"],
                front_default=pokemon_data["sprites"]["front_default"],
                front_female=pokemon_data["sprites"]["front_female"],
                front_shiny=pokemon_data["sprites"]["front_shiny"],
                front_shiny_female=pokemon_data["sprites"]["front_shiny_female"],
            )

            # do not verify that a property does not exist in defined types
            Statistic.objects.bulk_create(
                Statistic(
                    specie_id=pokemon.id,
                    name_id=query_statistic.get(name=dict_st["name"]).id,
                    value=dict_st["value"],
                )
                for dict_st in pokemon_data["stats"]
            )
