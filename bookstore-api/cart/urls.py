from django.template.context_processors import static
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/', views.CartAdd.as_view(), name='cart_add'),
    path('update/', views.CartUpdate.as_view(), name='cart_update'),
    path('delete/', views.CartDelete.as_view(), name='cart_delete'),
    path('get/', views.GetCart.as_view(), name='get-cart'),

]