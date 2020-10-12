from django.contrib.auth.models import User
from django.db import models

# Repeated code in models, fix once API tests are done


class Ability(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Move(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Specie(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)
    capture_rate = models.IntegerField()
    color = models.CharField(max_length=80)
    flavor_text = models.TextField()
    height = models.IntegerField()
    weight = models.IntegerField()
    abilities = models.ManyToManyField(Ability)
    moves = models.ManyToManyField(Move)
    types = models.ManyToManyField(Type)


class NameStatistic(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)


class Statistic(models.Model):
    """
    ...
    """

    # speed up the saved stage, if there is time to go back and convert to the table
    # name = models.CharField(max_length=80)
    name = models.ForeignKey(
        NameStatistic,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField()
    specie = models.ForeignKey(
        Specie,
        related_name="stats",
        on_delete=models.CASCADE,
    )


class Sprite(models.Model):
    """
    ...
    """

    back_default = models.URLField(max_length=200, null=True, blank=True)
    back_female = models.URLField(max_length=200, null=True, blank=True)
    back_shiny = models.URLField(max_length=200, null=True, blank=True)
    back_shiny_female = models.URLField(max_length=200, null=True, blank=True)
    front_default = models.URLField(max_length=200, null=True, blank=True)
    front_female = models.URLField(max_length=200, null=True, blank=True)
    front_shiny = models.URLField(max_length=200, null=True, blank=True)
    front_shiny_female = models.URLField(max_length=200, null=True, blank=True)
    specie = models.OneToOneField(
        Specie,
        related_name="sprites",
        on_delete=models.CASCADE,
    )


class Captured(models.Model):
    """
    ...
    """

    nick_name = models.CharField(max_length=80)
    is_party_member = models.BooleanField()
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
