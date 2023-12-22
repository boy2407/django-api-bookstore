from django.db import models
from django.conf import settings
from store.models import Book

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pricesale = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.quantity} of {self.book.name} by {self.user.username}'


# Create your models here.
