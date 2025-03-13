from django.urls import path
from . import views

urlpatterns = [
    path("art/create/", views.artwork_views.ArtCreateView.as_view(), name="art-create"),
    path("art/delete/<str:pk>/", views.artwork_views.ArtDelete.as_view(), name="art-delete"),
]
