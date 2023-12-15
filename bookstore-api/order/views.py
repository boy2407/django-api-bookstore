from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from cart.cart import Cart
from django.template.loader import render_to_string
from .forms import OrderCreateForm, AddressCreateForm
from .models import Order, OrderItem,Address
from django.contrib import messages

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated:

        customer = get_object_or_404(User, id=request.user.id)
        addr = Address.objects.filter(user_id=request.user.id).order_by('-create').first()

        order_form = OrderCreateForm(request.POST or None, initial={
            "name": customer.first_name + " " + customer.last_name,
            "email": customer.email
        })

        address_form = AddressCreateForm(request.POST or None, instance=addr)

        if request.method == 'POST':

            if order_form.is_valid() and address_form.is_valid():

                order = order_form.save(commit=False)
                address = address_form.save()

                address.user = customer
                order.customer = User.objects.get(id=request.user.id)
                order.address = address
                address.user = customer
                order.user = customer
                order.phone = address.phone
                # total
                order.payable = cart.get_total_price() - cart.get_total_discount()
                order.totalbook = len(cart)  # len(cart.cart) // number of individual book
                order.save()
                address.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

                if order.payment_method =='Chuyển khoản':
                    return render(request, "payment/payment.html", {"title": "Thanh toán",
                                                                                        'order_id':order.id,
                                                                                        'amount':order.payable,
                                                                                        'order_desc':f'Thanh toán hóa đơn {order.id}|Hiệu Sách Miền Tây'})

                # # Send Email
                send_mail_success_payment(cart=cart,order=order,address=address)
                # subject_2 = "Đặt Hàng Thành Công"
                # message_2 = render_to_string('order/send2.html', {
                #     'Product': cart,
                #     'MaDon':  str(order.id),
                #     'NgayDat': order.create,
                #     'CustomerName': order.name,
                #     'Address': address.city + ", " + address.district + ', ' + address.address,
                #     'Phone': order.phone,
                #     'Email': order.email,
                #     'TongTien': order.payable,
                #     'TypePay': order.payment_method,
                # })
                # send_mail(
                #     subject_2,
                #     '',
                #     'nguyentrongnghiadap2020@gmail.com',
                #     [order.email],
                #     fail_silently=False,
                #     html_message=message_2
                # )
                #
                # subject = "Đơn Hàng Cần Sử Lý"
                # message = render_to_string('order/send1.html', {
                #     'Product': cart,
                #     'MaDon':  str(order.id),
                #     'NgayDat': order.create,
                #     'CustomerName': order.name,
                #     'Address': address.city + ", " + address.district + ', ' + address.address,
                #     'Phone': order.phone,
                #     'Email': order.email,
                #     'TongTien': order.payable,
                #     'TypePay': order.payment_method,
                # })
                # send_mail(
                #     subject,
                #     '',
                #     'nguyentrongnghiadap2020@gmail.com',
                #     ['22550011@gm.uit.edu.vn'],
                #     fail_silently=False,
                #     html_message=message
                # )

                cart.clear()
                return render(request, 'store/successfull.html', {'order': order})
            else:
                messages.error(request, "Fill out your information correctly.")


        if len(cart)  > 0:
            return render(request, 'order/order.html', {"order_form": order_form, "address_form": address_form})
        else:
            return redirect('store:index')

    else:
        return redirect('login')
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
