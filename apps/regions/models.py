from django.db import models

from apps.pokemons.models import Specie

# Create your models here.


class Region(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)


class Location(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)
    region = models.ForeignKey(
        Region,
        related_name="locations",
        on_delete=models.CASCADE,
    )


class Area(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)
    location = models.ForeignKey(
        Location,
        related_name="areas",
        on_delete=models.CASCADE,
    )
    pokemons = models.ManyToManyField(Specie)
