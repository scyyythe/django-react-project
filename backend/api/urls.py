from django.urls import path
from .views.artwork_views import ArtCreateView, ArtListView,ArtUpdateView, ArtDeleteView, ArtDetailView
from .views.user_views import RetrieveUserView, UpdateUserView, DeleteUserView
from .views.filter import ArtSearchAndFilterView
from api.views.interaction import CommentCreateView, LikeCreateView, CartItemCreateView, CartItemDeleteView,CartRetrieveView

urlpatterns = [
    # user urls
    path('user/<str:pk>/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('user/<str:pk>/update/', UpdateUserView.as_view(), name='update_user'),
    path('user/<str:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    
    # artwork url
    path("art/create/", ArtCreateView.as_view(), name="art-create"),
    path('art/list/', ArtListView.as_view(), name='list_art'),
    path('art/<str:pk>/', ArtDetailView.as_view(), name='detail_art'),
    path('art/<str:pk>/update/', ArtUpdateView.as_view(), name='update_art'),
    path('art/<str:pk>/delete/', ArtDeleteView.as_view(), name='delete_art'),
    
    # interactions
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    
    # search/filter
    path('artworks/search/', ArtSearchAndFilterView.as_view(), name='artwork_search_filter'),
    
    # cart
    path('artworks/cart/', CartItemCreateView.as_view(), name='cart_item_create'),
    path('artworks/cart/owned/', CartRetrieveView.as_view(), name='retrieve_cart'),
    path('artworks/cart/remove/', CartItemDeleteView.as_view(), name='cart_item_remove'),
    
]
