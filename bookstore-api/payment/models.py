from django.db import models
from django.contrib.auth.models import User
from order.models import Order
# Create your models here.
class payment_Vnpay(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    order_desc = models.CharField(max_length=200,null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    vnp_PayDate = models.DateTimeField(auto_now_add=True)
    vnp_TransactionNo = models.CharField(max_length=200,null=True, blank=True)
    vnp_ResponseCode = models.CharField(max_length=200,null=True, blank=True)
    vnp_TmnCode = models.CharField(max_length=200,null=True, blank=True)
    vnp_BankCode = models.CharField(max_length=200,null=True, blank=True)