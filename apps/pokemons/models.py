import random

from django.contrib.auth.models import User
from django.db import models

# Repeated code in models, fix once API tests are done

STATE_MODIFICER = {
    "sleep": 20,
    "freeze": 20,
    "paralyze": 5,
    "sleep": 5,
    "poison": 5
}


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

    def __str__(self):
        return self.name

    def catch_percentage(self, current_hp = 0) -> int:
        """
        Capture Method (Generation II):

            (3 x Bmax - 2 x Bcurrent) x R
        Ω = ------------------------------
                (3 x Bmax) + Pstatus

        beta_max - The maximum HP of the targeted Pokémon
        beta_current - The current HP of the targeted Pokémon
        Pstatus - The modifier for any status condition the Pokémon has
        10 for sleep or freeze, 5 for paralyze, poison, or burn, 0 otherwise
        R - The catch rate of a Pokémon.

        Keyword Arguments:
            current_hp {number} -- [description] (default: {0})

        Returns:
            int -- [description]
        """

        max_hp = 0
        capture_rate = self.capture_rate

        try:
            max_hp = self.stats.get(name__name="hp").value
        except:
            return 0

        if current_hp <= 0 or current_hp > max_hp:
            current_hp = max_hp

        dividend = ((3 * max_hp) - (2 * current_hp)) * capture_rate
        divider = (3 * max_hp) # state modifier not applied

        omega = dividend / divider
        return omega


class NameStatistic(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name.name


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

    @staticmethod
    def active_member_limit() -> int:
        """
        returns the active member limit,
        this value can be obtained from env, db, etc.

        Returns:
            number -- [description]
        """
        return 6

    def start_capture(self) -> bool:
        """
        
        Note: 
        that choosing the name of this method calls
        into question renaming this model, which does
        not allow for correct semantics
        
        Capture.start_capture()
        Capture.capture()

        None good

        Returns:
            bool -- [description]
        """
        try:
            percent = self.specie.catch_percentage()
            return random.randrange(100) < percent
        except:
            return False
