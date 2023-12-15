from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address  # giả sử rằng model Address được định nghĩa trong tệp models.py cùng thư mục


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address', 'city', 'district','phone']