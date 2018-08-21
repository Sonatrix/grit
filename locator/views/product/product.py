from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Brand, Product

def branded_product(request, name):
    brand = Brand.objects.select_related().get(slug=name)
    products = Product.objects.prefetch_related().filter(brand_id=brand.id)
    product_filter = ProductFilter(request.GET, queryset=products)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_filter.qs, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    
    return render(request, 'locator/product/product_category.html', {"filter":product_filter, "products": numbers})