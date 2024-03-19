from django.urls import path
from mung_manager.pet_kindergardens.apis.views import (
    PetKindergardenListView,
    PetKindergardenProfileView,
    PetKindergardenSearchView,
)

urlpatterns = [
    path("", PetKindergardenListView.as_view(), name="pet-kindergarden-list"),
    path("/search", PetKindergardenSearchView.as_view(), name="pet-kindergarden-search"),
    path("/<int:pet_kindergarden_id>/profile", PetKindergardenProfileView.as_view(), name="pet-kindergarden-profile"),
]
