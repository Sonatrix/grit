from django.shortcuts import render
from .models import Product, Category

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {"products": products, "categories": categories})
    