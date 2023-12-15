from django.template.context_processors import static
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cart_details, name='cart-details'),
    path('cart-add/', views.cart_add, name='cart-add'),
    path('totalcart/', views.total_cart, name='totalcart'),
    path('cart-summary/', views.cart_summary, name='cart-summary'),
    path('cart-del/', views.cart_del, name='cart-del'),
    path('cart-remove/', views.cart_delete, name='cart-remove'),
    path('cart-update/', views.cart_update, name='cart-update'),
    path('item-total-price/', views.cart_update, name='item-total-price'),

]