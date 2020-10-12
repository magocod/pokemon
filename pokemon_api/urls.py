"""pokemon_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.authtoken import views

from django.contrib import admin
from django.urls import include, path

from apps.pokemons.urls import urlpatterns as pokemons_urls
from apps.regions import views as regions_views
from apps.users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.obtain_auth_token, name="api_login"),
    path("logout/", users_views.Logout.as_view(), name="api_logout"),
    path("pokemons/", include(pokemons_urls)),
    path("regions/", regions_views.RegionList.as_view(), name="regions_list"),
    path("regions/<int:pk>/", regions_views.RegionDetail.as_view() , name="region_detail"),
    path("locations/<int:pk>/", regions_views.LocationDetail.as_view(), name="location_detail"),
    path("areas/<int:pk>/", regions_views.AreaDetail.as_view(), name="area_detail"),
]
