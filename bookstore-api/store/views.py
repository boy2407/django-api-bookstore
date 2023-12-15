from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import Review
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Slider, Category,Writer
from .forms import  ReviewForm
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    newpublished = Book.objects.order_by('-created')[:10]
    discountbooks = Book.objects.filter(pricesale__gt=0).order_by('-pricesale')[:10]
    slide = Slider.objects.order_by('-created')[:3]
    category = Category.objects.all()
    context = {

        "newbooks": newpublished,
        "slide": slide,
        "discountbooks":discountbooks
    }
    return render(request, 'store/index.html', context)


def get_book(request, id):

    review = ReviewForm(request.POST or None)
    book = get_object_or_404(Book, id=id)
    rbooks = Book.objects.filter(category_id=book.category.id)

    r_review = Review.objects.filter(book_id=id).order_by('-created')

    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if review.is_valid():
                temp = review.save(commit=False)

                temp.customer = User.objects.get(id=request.user.id)
                temp.book = book

                temp = Book.objects.get(id=id)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                review.save()
                temp.save()
                messages.success(request, "Review Added Successfully")
                review = ReviewForm()
        else:
            messages.error(request, "You need login first.")

    context = {
        "book":book,
        "rbooks": rbooks,
        "form": review,
        "rreview": rreview
    }

    return render(request, "store/book.html", context)


def get_book_category(request,id):
    book_ = Book.objects.filter(category_id=id)
    paginator = Paginator(book_, 5)
    page = request.GET.get('page')
    book = paginator.get_page(page)
    return render(request, "store/category.html", {"book": book})

def get_writer(request, id):
    writer = get_object_or_404(Writer, id = id)
    books =Book.objects.filter(writer_id=writer.id)
    context ={
        'writer':writer,
        'books':books
    }
    return render(request, "store/writer.html", context)