from django.db import models

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
    region = models.ForeignKey(Region, related_name="region", on_delete=models.CASCADE,)


class Area(models.Model):
    """
    ...
    """

    name = models.CharField(max_length=80, unique=True)
    location = models.ForeignKey(Location, related_name="location", on_delete=models.CASCADE,)
