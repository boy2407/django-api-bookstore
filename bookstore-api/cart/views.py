from _decimal import Decimal
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from requests import Response
from rest_framework.views import APIView
from .cart import Cart
from store.serializers import  BookSerializer
from store.models import  Book
class CartAdd(APIView):
    def post(self, request):
        cart = Cart(request)
        id = int(request.data.get('id'))
        quantity = int(request.data.get('quantity'))
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "Sách không tồn tại"}, status=200)

        cart.add(book=book, quantity=quantity)
        count = cart.__len__()
        print(count)
        for item in cart :
           print(str(f"id :{item['book']['id']},name: {item['book']['name']} ,price: {item['book']['price']}, quantity: {item['quantity']} "))
        return JsonResponse({'status': 'success', 'message': "Thêm sản phẩm thành công", }, status=200)

class CartUpdate(APIView):
    def post(self, request):
        cart = Cart(request)
        id = int(request.data.get('id'))
        quantity = int(request.data.get('quantity'))

        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'success', 'message': "Sách không tồn tại"}, status=200)

        cart.update(book=book, quantity=quantity)
        count = cart.__len__()
        print(count)

        return JsonResponse({'status': 'success', 'message': "Thêm sản phẩm thành công"}, status=200)

class CartDelete(APIView):
    def post(self, request):
        cart = Cart(request)
        id = int(request.data.get('id'))

        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "Sách không tồn tại"}, status=200)

        cart.delete(book=book)
        return JsonResponse({'status': 'success', 'message': "Xóa phẩm thành công"}, status=200)


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
