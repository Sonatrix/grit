from django.urls import path
from locator.views import home, search

app_name = 'locator'

urlpatterns = [
    path('', home.index, name = 'home'),
    path('products/<slug:slug>/', home.product_details, name='product_detail'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('<slug:slug>/', home.product_category, name='category_products'),
]
