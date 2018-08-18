from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Product, Category


def index(request):
    products = Product.objects.prefetch_related().all().order_by('?')[:5]
    return render(request, 'locator/index.html', {"products": products})


def product_details(request, slug, pslug):
    product = get_object_or_404(Product, slug=pslug)
    latest_products = Product.objects.prefetch_related().filter(
        category_id=product.category_id).exclude(slug=pslug)[:5]

    return render(request, 'locator/product/product_details.html', {"product": product, 'latest_products': latest_products})


def product_category(request, slug):
    category = Category.objects.select_related().get(slug=slug)
    products = None

    if category.parent_id is not None:
        products = Product.objects.prefetch_related().filter(category_id=category.id)

    else:
        category_ids = Category.objects.all().filter(
            id=category.id).values_list("children__id", flat=True).distinct()
        products = Product.objects.prefetch_related().filter(category__in=category_ids).order_by('?')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'locator/product/product_category.html', {"products": numbers, "name": slug})
