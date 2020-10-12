from django.urls import path

from apps.pokemons import views

urlpatterns = [
    path("<int:pk>/", views.SpecieDetail.as_view(), name="specie_detail"),
    path("own/", views.CapturedList.as_view(), name="capture_list_create"),
    path("own/<int:pk>/", views.CapturedDetail.as_view(), name="capture_edit"),
    path("own/party/", views.CapturedParty.as_view(), name="capture_party_list"),
    path("own/swap/", views.SwapPartyMember.as_view(), name="capture_swap_party_member")
]
