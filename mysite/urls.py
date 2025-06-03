from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('catalog/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('about/', AboutView.as_view(), name='about'),
    path('address/', update_user_address_view, name='address'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('contact/', ContactsView.as_view(), name='contact'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('offer/', create_order_view, name='offer'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('loginview/', loginview, name='loginview'),
    path('logout/', logoutview, name='logout'),
    path('delete_favorite/<int:pk>', delete_or_add_favorite, name='del_fav'),
    path('add_product/<int:pk>', add_basket, name='add_cart'),
    path('remove_product/<int:pk>', remove_basket, name='del_cart'),
    path('payment/callback/', payment_callback_view, name='payment_callback'),
    path('payment/fail/', fail_freedom_pay, name='payment_fail'),
    path('payment/success/', success_freedom_pay, name='payment_success'),
    path('submit-contact-form/', submit_contact_form, name='submit_contact_form'),
]