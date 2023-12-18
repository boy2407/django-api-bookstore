from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .api_view import *

app_name = 'store'
urlpatterns = ([

                   path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
                   path('books-by-category/<int:category_id>/', BooksByCategory.as_view(), name='books-by-category'),

                   path('books-by-writer/<int:writer_id>/', BooksByWriter.as_view(), name='books-by-writer'),
                   path('writer/<int:pk>/', WriterDetail.as_view(), name='books-by-writer'),

                   path('categories/', CategoryList.as_view(), name='category-list'),
                   path('sliders/', SliderList.as_view(), name='slider-list'),

                   path('reviews-by-book/<int:book_id>', ReviewsByBook.as_view(), name='reviews-by-book'),
                   path('create-review/<int:book_id>', CreateReview.as_view(), name='create-review'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

