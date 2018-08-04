from django.urls import path, re_path, include
from locator.views import home, search
from django.contrib.sitemaps.views import sitemap
from locator.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap
}

app_name = 'locator'

urlpatterns = [
    path('', home.index, name = 'home'),
    re_path(r'^sitemap\.xml/$', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('<slug:slug>/', include([
        path('', home.product_category, name='category_products'),
        path('<slug:pslug>/', home.product_details, name='product_detail'),
    ])),
    
]
