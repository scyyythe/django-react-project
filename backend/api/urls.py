from django.urls import path
from . import views
from .views.artwork_views import ArtCreateView
from .views.user_views import RetrieveUserView, UpdateUserView, DeleteUserView

urlpatterns = [
    # user urls
    path('user/<str:pk>/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('user/<str:pk>/update/', UpdateUserView.as_view(), name='update_user'),
    path('user/<str:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    
    # artwork url
    path("art/create/", ArtCreateView.as_view(), name="art-create"),
]
