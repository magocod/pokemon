from django.contrib import admin

from apps.pokemons.models import (
    Ability,
    Move,
    Pokemon,
    Sprite,
    Statistic,
    Type,
    TypeStatistic,
)

# Register your models here.

admin.site.register(Ability)
admin.site.register(Move)
admin.site.register(Pokemon)
admin.site.register(Sprite)
admin.site.register(Statistic)
admin.site.register(Type)
admin.site.register(TypeStatistic)
