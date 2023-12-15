from django import forms
from .models import Order,Address
class AddressCreateForm(forms.ModelForm):
    # Your existing fields...
    CTY_CHOICES = (
        ('Tp Hcm', 'Tp Hcm'),
    )

    DISCRICT_CHOICES = (
        ('Quận 1', 'Quận 1'),
        ('Quận 3', 'Quận 3'),
        ('Quận 2', 'Quận 2'),
    )

    city = forms.ChoiceField(choices=CTY_CHOICES)
    district = forms.ChoiceField(choices=DISCRICT_CHOICES)
    class Meta:
        model = Address
        fields = ['address', 'phone', 'city', 'district',]

class OrderCreateForm(forms.ModelForm):

    PAYMENT_METHOD_CHOICES = (
        ('COD', 'COD'),
        ('Chuyển khoản', 'Chuyển khoản')
    )
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'payment_method', ]
