from django.urls import path
from .views import *


urlpatterns = [
    path('', ProductListApiView.as_view()),
    path('<int:pk>/', ProductDetailApiView.as_view()),
    path('rec/', ProductOnly3ApiView.as_view()),
    path("update_categories/", update_categories),
    path('categories/', CategoriesListApiView.as_view()),
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-detail'),
    path('cart/add/', CartViewSet.as_view({'post': 'add_product'}), name='cart-add'),
    path('cart/remove/', CartViewSet.as_view({'post': 'remove_product'}), name='cart-remove'),
    path('favorites/', FavoriteViewSet.as_view({'get': 'list', 'post': 'create',}), name='favorite-list'),
    path('favorites/<int:pk>/', FavoriteViewSet.as_view({'delete': 'destroy',}), name='favorite-detail'),
]
