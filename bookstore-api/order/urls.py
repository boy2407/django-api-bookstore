from django.urls import path
from . import views
app_name = 'order'
urlpatterns = [
    path('order-create/', views.order_create, name="order-create"),
    path('order-list/', views.order_list, name="order-list"),
]
