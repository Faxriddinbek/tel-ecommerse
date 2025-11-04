from django_filters import rest_framework as django_filters # qayta nomalash
from products.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='prise', lookup_expr='gte')# lookup_expr='gte' bu shu prisedan teng yoki katta
    max_price = django_filters.NumberFilter(field_name='prise', lookup_expr='lte')# lookup_expr='lte' bu shu prisega teng yoki kichkina

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']