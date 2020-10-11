from django.contrib import admin

from apps.regions.models import Area, Location, Region

# Register your models here.

admin.site.register(Region)
admin.site.register(Area)
admin.site.register(Location)
