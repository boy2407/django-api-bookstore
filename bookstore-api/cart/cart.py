from decimal import Decimal
from store.serializers import  BookSerializer
from store.models import  Book
from django.conf import settings

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        user_id = str(request.user.id)  # Lấy ID người dùng từ request
        cart = self.session.get(user_id)  # Sử dụng ID người dùng thay vì CART_SESSION_ID
        if not cart:
            cart = self.session[user_id] = {}
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, book, quantity):
        book_id = str(book.id)
        if book_id in self.cart:
            self.cart[book_id]['quantity'] += quantity
        else:
            self.cart[book_id] = {
                'quantity': quantity,
                'price': str(book.price),
                'pricesale': str(book.pricesale),
                'total_price': '0'
            }
        if self.cart[book_id]['pricesale'] > '0':
            self.cart[book_id]['total_price'] = str(Decimal(self.cart[book_id]['pricesale']) * int(self.cart[book_id]['quantity']))
        else:
            self.cart[book_id]['total_price'] = str(Decimal(self.cart[book_id]['price']) * int(self.cart[book_id]['quantity']))
        self.save()

    def update(self, book, quantity):

        book_id = str(book.id)
        self.cart[book_id]['quantity'] = quantity
        if self.cart[book_id]['pricesale'] > '0':
            self.cart[book_id]['total_price'] = str(
                Decimal(self.cart[book_id]['pricesale']) * int(self.cart[book_id]['quantity']))
        else:
            self.cart[book_id]['total_price'] = str(
                Decimal(self.cart[book_id]['price']) * int(self.cart[book_id]['quantity']))
        self.save()

    def item_total_price (self ,book):
        book_id = str(book.id)
        quantity  = self.cart[book_id]['quantity']
        price = self.cart[book_id]['price']
        return Decimal(price) * quantity

    def delete(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        for book in books:
            book_serializer = BookSerializer(book)
            self.cart[str(book.id)]['book'] = book_serializer.data

        for item in self.cart.values():
            item['price'] = str(Decimal(item['price']))
            item['pricesale'] = str(Decimal(item['pricesale']))
            if item['pricesale'] > '0':
                item['total_price'] = str(Decimal(item['pricesale']) * int(item['quantity']))
            else:
                item['total_price'] = str(Decimal(item['price']) * int(item['quantity']))
            yield item

    def get_cart(self):
        return self.cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_discount(self):
        total = 0
        for item in self.cart.values():
            if Decimal(item['pricesale']) > 0:
                total += (Decimal(item['price']) - Decimal(item['pricesale']))*item['quantity']
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

