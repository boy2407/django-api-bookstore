from rest_framework import serializers
from .models import Writer,Book,Review,Slider,Category

class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['id', 'name', 'slug', 'bio', 'pic', 'create_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [ 'review_star', 'review_text', 'created']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'
