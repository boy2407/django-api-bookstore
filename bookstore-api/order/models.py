from django.db import models
from django.contrib.auth.models import User
from store.models import  Book
# Create your models here.
class Address (models.Model):

    address = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=16)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Address'
    def __str__(self):
        return 'Address - ' + str(self.id)


class Order (models.Model) :

  user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
  address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)

  name = models.CharField(max_length=30)
  phone = models.CharField(max_length=16)
  email = models.EmailField()
  payment_method = models.CharField(max_length=20)

  create = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)
  paid = models.BooleanField(default=False)

  totalbook = models.IntegerField()
  payable = models.DecimalField(max_digits=10, decimal_places=2)
  class Meta:
      ordering = ('-create',)

  def __str__(self):
      return 'Order {}'.format(self.id)
  def get_total_cost(self):
      return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model) :
  order = models.ForeignKey(Order,on_delete=models.CASCADE)
  book = models.ForeignKey(Book,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
      return '{}'.format(self.id)
  def get_cost(self):
         return self.price * self.quantity