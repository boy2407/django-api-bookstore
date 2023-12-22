from django.contrib import admin
from .models import Category, Writer, Book, Slider,Review
import locale

# Register your models here.
class AddCategory(admin.ModelAdmin):
    list_display = ['name', 'slug']
# prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, AddCategory)

class BookInline(admin.TabularInline):
    model = Book
    # extra = 1  # số lượng formset hiển thị mặc định
class AddWriter(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BookInline]

admin.site.register(Writer, AddWriter)


class AddBook(admin.ModelAdmin):
    list_display = ['name','price','pricesale', 'stock', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated', 'category', 'writer']
    list_editable = ['price', 'pricesale', 'stock', 'status']
    prepopulated_fields = {'slug': ('name',)}

    def prices(self, obj):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(obj.price, grouping=True)

    prices.short_description = 'price'


admin.site.register(Book, AddBook)

admin.site.register(Slider)

admin.site.register(Review)