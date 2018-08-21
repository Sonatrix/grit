from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Collection
from locator.filters import ProductFilter

def collections(request, name):
    collection = Collection.objects.prefetch_related().get(slug=name)
    if collection is not None:
        product_list = collection.products
    else:
        product_list = None

    product_filter = ProductFilter(request.GET, queryset=product_list)
    productsData = product_filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(productsData, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    
    return render(request, 'locator/product/product_category.html', {"filter":product_filter,"products": numbers, "name": name})