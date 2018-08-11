from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Brand, Category, Product

def product_brand(request, name):
    brand = Brand.objects.select_related().get(slug=name)
    products = Product.objects.prefetch_related().filter(brand_id=brand.id)
    categories = Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    
    return render(request, 'locator/product/product_category.html', {"products": numbers, "categories": categories, "name": name})