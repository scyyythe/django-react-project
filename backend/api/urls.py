from django.urls import path
from . import views
from .views.artwork_views import ArtCreateView
urlpatterns = [
    path("art/create/", views.artwork_views.ArtCreateView.as_view(), name="art-create"),
]
