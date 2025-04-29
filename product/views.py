from django.shortcuts import render
from django.http import HttpResponse

from product.filters import ProductFilter
from product.models import Product, Category, Favorite
from product.pagination import MyCustomPagination
from product.serializers import ProductSerializer, CategorySerializers, FavoriteSerializer
from scripts.import_categories import import_categories_from_api
from scripts.import_images import import_product_images
from scripts.import_products import import_products_from_api
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer



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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    # search_fields = ('title', 'description')
    ordering_fields = ['price', 'updated']


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


class CategoriesListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Добавить товар в корзину",
        responses={201: CartItemSerializer(many=True)}
    )
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Добавить товар в корзину",
        request=CartItemSerializer,
        responses={201: CartItemSerializer}
    )
    def add_product(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartItemSerializer(item).data, status=201)

    @extend_schema(
        summary="Добавить товар в корзину",
        request=CartItemSerializer,
        responses={201: CartItemSerializer}
    )
    def remove_product(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({'status': 'Product removed'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=404)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Список избранных товаров",
        responses=FavoriteSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Добавить в избранное",
        request=FavoriteSerializer,
        responses=FavoriteSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Удалить из избранного",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)