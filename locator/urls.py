from django.urls import path, re_path, include
from locator.views import home, search

app_name = 'locator'

urlpatterns = [
    path('', home.index, name = 'home'),
    path('search/', search.SearchView.as_view(), name='search'),
    path('<slug:slug>/', include([
        path('', home.product_category, name='category_products'),
        path('<slug:pslug>/', home.product_details, name='product_detail'),
    ])),
    
]
