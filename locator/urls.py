from django.urls import path, re_path, include
from locator.views import home, search, common
from locator.views.product import product
from django.contrib.sitemaps.views import sitemap
from locator.sitemaps import ProductSitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'products': ProductSitemap,
    'posts': PostSitemap
}

app_name = 'locator'

urlpatterns = [
    path('', home.index, name='home'),
    re_path(r'^sitemap\.xml/$', sitemap,
            {'sitemaps': sitemaps}, name='sitemap'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('contact/', common.contact, name='contact'),
    path('brand/<slug:name>/', product.product_brand, name='brands'),
    path('<slug:slug>/', include([
        path('', home.product_category, name='category_products'),
        path('<slug:pslug>/', home.product_details, name='product_detail'),
    ])),
]
