from django.urls import path
from . import views
app_name = 'order'
urlpatterns = [
    path('createorder/', views.CreateOrder.as_view(), name="CreateOrder"),
    path('order-list/', views.order_list, name="order-list"),
]
