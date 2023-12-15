from .cart import Cart
def cart(request):
    cart = Cart(request)
    context = {
        "cart": cart
    }
    return context
