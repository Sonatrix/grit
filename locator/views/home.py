from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Product, Category

def index(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()
    return render(request, 'index.html', {"products": products, "categories": categories})

def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    latest_products = Product.objects.filter(category_id=product.category_id).exclude(slug=slug)[:5]
    return render(request, 'product/product_details.html', {"product": product, "categories": categories, 'latest_products': latest_products})

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
    return render(request, 'product/product_category.html', {"products": numbers, "categories": categories, "name": slug})