from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.middleware.csrf import rotate_token, get_token
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from .forms import RegistrationForm, UpdateUserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .token import user_tokenizer_generate
from django.contrib.auth.models import auth
from django.template.loader import render_to_string
from cart.models import Cart
from order.models import Address
from order.serializers import AddressSerializer
from .serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm
import json
from django.forms.models import model_to_dict
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f'registration: {data}')
        form = RegistrationForm(data)
        address_serializer = AddressSerializer(data=data)  # new line

        if form.is_valid() and address_serializer.is_valid():  # modified line
            user = form.save()
            address = address_serializer.save(user=user)  # new line
            # Email verification setup (template)
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('user/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })
            user.email_user(message=message, subject=subject)
            return JsonResponse({'status': 'success', 'message': 'Account created successfully,\n please check your email'},status=200)  # modified line
        else:
            errors = {}
            if not form.is_valid():
                errors = {**errors, **form.errors}
            if not address_serializer.is_valid():  # new line
                errors = {**errors, **address_serializer.errors}  # new line
            for field, error in errors.items():
                return JsonResponse({'status': 'error', 'field': field, 'error': error[0]}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def email_verification(request, uidb64, token):
    # uniqueid
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    # Failed
    else:
        return redirect('email-verification-failed')
def email_verification_sent(request):
    return render(request, 'user/registration/email-verification-sent.html')
def email_verification_success(request):
    return render(request, 'user/registration/email-verification-success.html')
def email_verification_failed(request):
    return render(request, 'user/registration/email-verification-failed.html')

@login_required
@csrf_exempt
def get_profile(request):
    if request.method == 'GET':
        customer = get_object_or_404(User, id=request.user.id)
        addresss = Address.objects.filter(user_id=request.user.id).order_by('-create').first()

        if customer is not None and addresss is not None:
            customer_serializer = UserSerializer(model_to_dict(customer))
            address_serializer = AddressSerializer(model_to_dict(addresss))
            print(customer_serializer.data)
            print(address_serializer.data)

            return JsonResponse({'status': 'success', 'user': customer_serializer.data, 'address': address_serializer.data}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'User or address not found.'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer = get_object_or_404(User, id=request.user.id)
        addresss = Address.objects.filter(user_id=request.user.id).order_by('-create').first()

        # Nếu address không tồn tại, tạo mới
        if addresss is None:
            addresss = Address(user=customer)

        fuser = UserSerializer(customer, data=data)
        faddress = AddressSerializer(addresss, data=data)

        if fuser.is_valid() and faddress.is_valid():
            fuser.save()
            faddress.save()
            return JsonResponse({'status': 'success', 'message': 'User profile updated.'})
        else:
            errors = {}
            if not fuser.is_valid():
                errors = {**errors, **fuser.errors}
            if not faddress.is_valid():
                errors = {**errors, **faddress.errors}
            for field, error in errors.items():
                return JsonResponse({'status': 'error', 'field': field, 'error': error[0]}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # user = get_object_or_404(User, username=username)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if user.is_active is False:
                return JsonResponse({'status': 'error',
                                            'message': 'Tài khoản chưa kích hoạt' + '\n' + 'Vui lòng kiểm tra email của bạn'},
                                            status=200)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                rotate_token(request)  # Generate a new CSRF token
                # Load the user's cart into the session

                user_cart = Cart.objects.filter(user=user)
                if not request.session.get(str(user.id)):
                    request.session[str(user.id)] = {}
                for item in user_cart:
                    request.session[str(user.id)][str(item.book.id)] = {'quantity': item.quantity, 'price': str(item.price),'pricesale': str(item.pricesale)}
                return JsonResponse({'csrfToken': get_token(request),'status': 'success', 'message': 'Đăng nhập thành công'},status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Mật khẩu không trùng khớp'}, status=200)
        else:
             # Người dùng không tồn tại, xử lý tình huống này
             return JsonResponse({'status': 'error', 'message': 'Tài khỏa của bạn không tồn tại'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            # Only save the cart into the database if it's not empty
            if str(request.user.id) in request.session:
                print("user có cart")
                # Save the user's cart into the database
                user_cart = Cart.objects.filter(user=request.user, ordered=False)
                user_cart.delete()  # Clear the old cart
                for key, value in request.session[str(request.user.id)].items():
                    Cart.objects.create(user=request.user, book_id=key, quantity=value['quantity'], price=value['price'],pricesale=value['pricesale'], ordered=False)


            for key in list(request.session.keys()):
                if key == 'session_key':
                    continue
                else:
                    del request.session[key]
        except KeyError:
            pass

        auth.logout(request)
        return JsonResponse({'status': 'success', 'message': 'User logged out.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
