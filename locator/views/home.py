from django.shortcuts import render, get_object_or_404, get_list_or_404
from locator.models import Product, Category

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {"products": products, "categories": categories})

def product_details(request, slug):
	product = get_object_or_404(Product, slug=slug)
	categories = Category.objects.all()
	return render(request, 'product/product_details.html', {"product": product, "categories": categories})

def product_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = get_list_or_404(Product, category_id=category.id)
    categories = Category.objects.all()
    return render(request, 'product/product_category.html', {"products": products, "categories": categories, "name": slug})