from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Book


# Create your views here.
def cart_add(request):
    if request.POST:
        cart = Cart(request)
        id = int(request.POST.get('id'))
        quantity = int(request.POST.get('quantity'))
        book = get_object_or_404(Book, id=id)
        cart.add(book=book, quantity=quantity)
        count = cart.__len__()
        return JsonResponse({'Success': True,
                             'msg': "Thêm sản phẩm thành công",
                             'count': count,
                             })

    return JsonResponse({'Success': False,
                         'msg': "Thêm hàng thất bại",
                         })


def cart_update(request):
    cart = Cart(request)
    id_str = request.POST.get('id')
    if id_str is not None:
        id = int(id_str)
        quantity = int(request.POST.get('quantity'))
        book = get_object_or_404(Book, id=id)
        cart.update(book=book, quantity=quantity)
        price = (book.price * quantity)
        return render(request, 'cart/price.html', {"price":price})


def cart_delete(request):
    cart = Cart(request)
    id = int(request.POST.get('id'))
    book = get_object_or_404(Book, id=id)
    cart.delete(book=book)
    return JsonResponse({'Success': True,
                         'msg': "Xóa phẩm thành công",
                         })


def item_total_price(request):
    return render(request, 'cart/newTotalItem.html')


def cart_summary(request):
    return render(request, 'cart/summary.html')


def total_cart(request):
    return render(request, 'cart/totalcart.html')


def cart_details(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'cart/cart.html', context)


def cart_del(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse('deleted successfully')
