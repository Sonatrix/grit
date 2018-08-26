from django_filters import FilterSet, RangeFilter, NumberFilter, ModelMultipleChoiceFilter
from locator.models import Product, Brand, Category
from django import forms
from django_filters.widgets import SuffixedMultiWidget

def brands(request):
	return Brand.objects.all()


def categories(request):
	return Category.published.exclude(parent=None).all()

class RangeWidget(SuffixedMultiWidget):
    suffixes = ['min', 'max']

class ProductFilter(FilterSet):
    price = RangeFilter()
    brand = ModelMultipleChoiceFilter(queryset=brands, widget=forms.CheckboxSelectMultiple)
    category = ModelMultipleChoiceFilter(queryset=categories, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = ['brand','price',]