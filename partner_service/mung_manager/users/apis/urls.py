from django.urls import path
from mung_manager.users.apis.views import UserProfileView

urlpatterns = [
    path("/profile", UserProfileView.as_view(), name="user-profile"),
]
