from django.shortcuts import render
from django.http import HttpResponse

from product.models import Product
from product.pagination import MyCustomPagination
from product.serializers import ProductSerializer
from scripts.import_categories import import_categories_from_api
from scripts.import_images import import_product_images
from scripts.import_products import import_products_from_api
from rest_framework import generics
from rest_framework.permissions import AllowAny


def update_categories(request):
    if import_categories_from_api():
        if import_products_from_api():
            if import_product_images():
                return HttpResponse('OK')
    return HttpResponse('Error')


class ProductListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    pagination_class = MyCustomPagination
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductOnly3ApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all().order_by('?')[:10]
    # pagination_class = MyCustomPagination
    serializer_class = ProductSerializer