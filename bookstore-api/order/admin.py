from django.contrib import admin
from .models import  Order,OrderItem,Address
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # extra = 1  # số lượng formset hiển thị mặc định


class AddOrder(admin.ModelAdmin):
    list_display = ['id','name' ,'user','phone','email','create']
    search_fields = ['name', 'phone', 'id', ]
    inlines = [OrderItemInline]
    # phân trang
    list_per_page = 20

class OrderInline(admin.TabularInline):
    model = Order
    # extra = 1  # số lượng formset hiển thị mặc định
class AddAddress(admin.ModelAdmin):
    inlines = [OrderInline]


admin.site.register(Order, AddOrder)
admin.site.register(Address,AddAddress)
admin.site.register(OrderItem)