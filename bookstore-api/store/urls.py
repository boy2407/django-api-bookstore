from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'
urlpatterns = ([
   path('', views.index, name="index"),
   path('book/<int:id>', views.get_book, name="book"),
   path('category/<int:id>', views.get_book_category, name="category"),
   path('writer/<int:id>', views.get_writer, name="writer"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
