from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from store.models import Book, Category, Writer
# truy vấn
from django.db.models import Q
from django.db.models.functions import Lower

def search(request):
    search = request.GET.get('search_book')
    books = Book.objects.all()
    if search:
        search = search.lower()
        books = books.annotate(
            lower_name=Lower('name'),
            lower_category_name=Lower('category__name'),
            lower_writer_name=Lower('writer__name'),
        ).filter(
            Q(lower_name__icontains=search)|
			Q(lower_category_name__icontains=search)|
            Q(lower_writer_name__icontains=search)
        )
    paginator = Paginator(books, 5)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {
        "book": books,
        "search": search,
    }
    return render(request, 'store/category.html', context)


