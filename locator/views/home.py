from django.shortcuts import render, get_object_or_404, get_list_or_404
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
    return render(request, 'product/product_category.html', {"products": products, "categories": categories, "name": slug})