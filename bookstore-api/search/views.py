from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from store.models import Book, Category, Writer
from store.serializers import BookSerializer
from rest_framework.filters import SearchFilter
class BookSearchView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category__name', 'writer__name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data})
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data})