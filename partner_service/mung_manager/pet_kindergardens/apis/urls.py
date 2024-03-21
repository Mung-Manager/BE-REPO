from django.urls import path
from mung_manager.pet_kindergardens.apis.pet_kindergardens.views import (
    PetKindergardenListView,
    PetKindergardenProfileView,
    PetKindergardenSearchView,
)
from mung_manager.pet_kindergardens.apis.tickets.views import (
    PetKindergardenTicketDetailView,
    PetKindergardenTicketListView,
)

urlpatterns = [
    # pet kindergarden
    path("", PetKindergardenListView.as_view(), name="pet-kindergarden-list"),
    path("/search", PetKindergardenSearchView.as_view(), name="pet-kindergarden-search"),
    path("/<int:pet_kindergarden_id>/profile", PetKindergardenProfileView.as_view(), name="pet-kindergarden-profile"),
    # ticket
    path("/<int:pet_kindergarden_id>/tickets", PetKindergardenTicketListView.as_view(), name="pet-kindergarden-tickets-list"),
    path(
        "/<int:pet_kindergarden_id>/tickets/<int:ticket_id>",
        PetKindergardenTicketDetailView.as_view(),
        name="pet-kindergarden-tickets-detail",
    ),
]
