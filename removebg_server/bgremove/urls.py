from django.urls import path
from .views import upload_image, remove_background

urlpatterns = [
    path("upload/", upload_image, name="upload_image"),
    path("removebg/", remove_background, name="remove_background"),
]
