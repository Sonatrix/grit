from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Product, Category
from django.utils.text import slugify

def index(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()
    return render(request, 'locator/index.html', {"products": products, "categories": categories})

def product_details(request, slug, pslug):
    product = get_object_or_404(Product, slug=pslug)
    categories = Category.objects.all()
    category = Category.objects.select_related().get(id=product.category_id)
    latest_products = Product.objects.filter(category_id=product.category_id).exclude(slug=pslug)[:5]
    return render(request, 'locator/product/product_details.html', {"product": product, "categories": categories, "path": slugify(category), 'latest_products': latest_products})

def product_category(request, slug):
    category = Category.objects.select_related().get(slug=slug)
    products = get_list_or_404(Product, category_id=category.id)
    categories = Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'locator/product/product_category.html', {"products": numbers, "categories": categories, "path": slugify(category), "name": slug})