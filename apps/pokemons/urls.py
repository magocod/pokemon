from django.urls import path

from apps.pokemons import views

urlpatterns = [
	path('<int:pk>/', views.SpecieDetail.as_view()),
]
