from django.urls import path
from mung_manager.files.apis.views import FileUploadAPI

urlpatterns = [
    path("/upload", FileUploadAPI.as_view(), name="file-upload"),
]
