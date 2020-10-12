from django.urls import path

from apps.pokemons import views

urlpatterns = [
    path("<int:pk>/", views.SpecieDetail.as_view()),
    path("own/", views.CapturedList.as_view()),
    path("own/<int:pk>/", views.CapturedDetail.as_view()),
    path("own/party/", views.CapturedParty.as_view()),
]
