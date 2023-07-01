from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    # Performs a case - insensitive search for records where the field contains the given value.
    name = filters.CharFilter(lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price']