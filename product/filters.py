import django_filters

from product.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="sale_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="sale_price", lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), field_name='category')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']