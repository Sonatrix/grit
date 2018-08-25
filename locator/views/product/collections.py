from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from locator.models import Collection
from locator.filters import ProductFilter


def collections(request, name):
    try:
        collection = Collection.objects.select_related().get(slug=name)
        product_list = collection.products
    except ObjectDoesNotExist:
        collection = None
        product_list = None

    product_filter = ProductFilter(request.GET, queryset=product_list)
    productsData = product_filter.qs.order_by("?")
    page = request.GET.get('page', 1)
    paginator = Paginator(productsData, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'locator/product/product_category.html', {"filter": product_filter, "products": numbers, "name": name})

def collections_view(self):
    return redirect('locator:home')