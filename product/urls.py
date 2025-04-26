from django.urls import path
from .views import *


urlpatterns = [
    path('', ProductListApiView.as_view()),
    path('<int:pk>/', ProductDetailApiView.as_view()),
    path('rec/', ProductOnly3ApiView.as_view()),
    path("update_categories/", update_categories),
    path('categories/', CategoriesListApiView.as_view())
]
