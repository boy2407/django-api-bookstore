from _pydecimal import Decimal

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from cart.cart import Cart
from django.template.loader import render_to_string
from rest_framework.reverse import reverse

from .forms import OrderCreateForm, AddressCreateForm
from .models import Order, OrderItem,Address
from store.models import Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rt_status
# Create your views here.

class CreateOrder(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        address_id = request.data.get('address_id')
        payment_method = request.data.get('payment_method')

        if user_id and address_id and payment_method:

            customer = get_object_or_404(User, id=user_id)
            addr = get_object_or_404(Address, id=address_id)
            cart = Cart(request)
            for item in cart:
                item['total_price'] = item['quantity'] * item['book']['pricesale'] if item['book']['pricesale'] > 0 else item['quantity'] * item['book']['price']
                print(f"id: {item['book']['id']}, name: {item['book']['name']}, price: {item['book']['price']}, quantity: {item['quantity']}, total price: {item['total_price']}")

            order = Order()
            order.customer = customer
            order.address = addr
            order.user = customer
            order.name = customer.first_name + " "+customer.last_name
            order.phone = addr.phone
            order.email = customer.email
            order.payment_method = payment_method
            # # total
            order.payable = cart.get_total_price() + 30_000
            order.totalbook = len(cart)  # len(cart.cart) // number of individual book
            order.save()

            for item in cart:
                book = Book.objects.get(id=item['book']['id'])
                OrderItem.objects.create(
                    order=order,
                    book=book,
                    price=item['price'],
                    quantity=item['quantity']
                )
            if order.payment_method == 'Chuyển khoản':
                # Tạo URL thanh toán tại đây. Đảm bảo rằng URL này dẫn đến trang thanh toán của bạn.
                payment_url = request.build_absolute_uri(reverse(
                    'payment:payment')) + f"?title=Thanh%20toán&order_id={order.id}&amount={order.payable}&order_desc=Thanh%20toán%20hóa%20đơn%20{order.id}|Hiệu%20Sách%20Miền%20Tây"

                return JsonResponse(
                    {"status": "success", "message": "Order created successfully", "payment_url": payment_url},
                    status=200)

            # # Send Email
            send_mail_success_payment(cart=cart, order=order, address=addr)
            # cart.clear()

            return Response({"status": "success", "message": "Order created successfully"},
                            status=200)
        else:
            return Response({"status": "error", "message": "Invalid user_id, address_id or payment_method"},
                            status=200)

def order_list(request):
	order = Order.objects.filter(user_id = request.user.id).order_by('-create')
	paginator = Paginator(order, 5)
	page = request.GET.get('page')
	order_list = paginator.get_page(page)

	return render(request, 'order/list.html', {"order": order_list})

def send_mail_success_payment(cart,order,address):
    subject_2 = "Đặt Hàng Thành Công"
    message_2 = render_to_string('order/send2.html', {
        'Product': cart,
        'MaDon': str(order.id),
        'NgayDat': order.create,
        'CustomerName': order.name,
        'Address': address.city + ", " + address.district + ', ' + address.address,
        'Phone': order.phone,
        'Email': order.email,
        'TongTien': order.payable,
        'TypePay': order.payment_method,
    })
    send_mail(
        subject_2,
        '',
        'nguyentrongnghiadap2020@gmail.com',
        [order.email],
        fail_silently=False,
        html_message=message_2
    )

    subject = "Đơn Hàng Cần Sử Lý"
    message = render_to_string('order/send1.html', {
        'Product': cart,
        'MaDon': str(order.id),
        'NgayDat': order.create,
        'CustomerName': order.name,
        'Address': address.city + ", " + address.district + ', ' + address.address,
        'Phone': order.phone,
        'Email': order.email,
        'TongTien': order.payable,
        'TypePay': order.payment_method,
    })
    send_mail(
        subject,
        '',
        'nguyentrongnghiadap2020@gmail.com',
        ['22550011@gm.uit.edu.vn'],
        fail_silently=False,
        html_message=message
    )
