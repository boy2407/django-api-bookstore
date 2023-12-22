from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from .cart import Cart
from store.models import Book
from rest_framework import status
class GetCart(APIView):
    def get(self, request):
        try:
            cart = Cart(request)
            for item in cart:
                print(
                    str(f"id: {item['book']['id']},name: {item['book']['name']} ,price: {item['book']['price']}, quantity: {item['quantity']} ,total price: {item['total_price']}"))
            return JsonResponse({'status': 'success', 'message': 'success cart', 'cart': cart.get_cart()},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        for item in cart:
            print(
                str(f"id: {item['book']['id']},name: {item['book']['name']} ,price: {item['book']['price']}, quantity: {item['quantity']} ,total price: {item['total_price']}"))

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


def cart_del(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponse('deleted successfully')
