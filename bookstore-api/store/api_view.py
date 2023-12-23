from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Writer, Book, Review, Slider, Category
from .serializers import WriterSerializer, BookSerializer, ReviewSerializer, SliderSerializer, CategorySerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse({'status': 'success', 'book': serializer.data} ,status=200)


class BooksByCategory(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(category_id=self.kwargs['category_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data}, status=200)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)

class NewBooks(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.order_by('-created')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data}, status=200)
        serializer = self.get_serializer(queryset, many=True)

        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class BestSellerBook(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.order_by('stock')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data}, status=200)
        serializer = self.get_serializer(queryset, many=True)

        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data}, status=200)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class SliderList(generics.ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data}, status=200)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class ReviewsByBook(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data})
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class WriterDetail(generics.RetrieveAPIView):
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class BooksByWriter(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(writer_id=self.kwargs['writer_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'status': 'success', 'data': serializer.data})
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)


class CreateReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user, book=book)
            return JsonResponse({'status': 'success', 'message': 'Review created.', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
        else:
            errors = {}
            for field, error in serializer.errors.items():
                errors[field] = error[0]
            return JsonResponse({'status': 'error', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
