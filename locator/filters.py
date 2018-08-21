from django_filters import FilterSet, RangeFilter, NumberFilter, ModelMultipleChoiceFilter
from locator.models import Product, Brand
from django import forms
from django_filters.widgets import SuffixedMultiWidget

def brands(request):
	print(request)
	return Brand.objects.all()

class RangeWidget(SuffixedMultiWidget):
    suffixes = ['min', 'max']

class ProductFilter(FilterSet):
    price = RangeFilter()
    brand = ModelMultipleChoiceFilter(queryset=brands, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = ['brand','price',]