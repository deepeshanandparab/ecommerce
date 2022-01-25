from django.forms import TextInput
from .models import Product
import django_filters

class ProductSearch(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput
                                        (
                                          attrs={
                                              'autocomplete' : 'false',
                                                 }),label='')

    class Meta:
        model = Product
        fields = ['name']