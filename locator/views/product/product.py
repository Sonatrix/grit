from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from locator.filters import ProductFilter
from locator.models import Brand, Product


def branded_product(request, name):
    try:
        brand = Brand.objects.select_related().get(slug=name)
        products = Product.objects.prefetch_related().filter(
            brand_id=brand.id).order_by("?")
    except ObjectDoesNotExist:
        brand = None
        products = None

    product_filter = ProductFilter(request.GET, queryset=products)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_filter.qs, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'locator/product/product_category.html', {"filter": product_filter, "products": numbers})
