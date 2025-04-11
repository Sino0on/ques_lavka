from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImageProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializers()
    images_product = ImageProductSerializers(many=True, source='images')

    class Meta:
        model = Product
        fields = '__all__'
        include = 'images'

