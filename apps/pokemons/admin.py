from django.contrib import admin

from apps.pokemons.models import (
    Ability,
    Move,
    NameStatistic,
    Specie,
    Sprite,
    Statistic,
    Type,
)

# Register your models here.

admin.site.register(Ability)
admin.site.register(Move)
admin.site.register(Specie)
admin.site.register(Sprite)
admin.site.register(Statistic)
admin.site.register(Type)
admin.site.register(NameStatistic)
