from django_filters.rest_framwork import FilterSet

from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'inventory': ['gt', 'lt',],
        }
