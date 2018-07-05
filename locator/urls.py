from django.urls import path
from locator.views import home

app_name = 'locator'

urlpatterns = [
    path('', home.index, name = 'home'),
    path('products/<slug:slug>/', home.product_details, name='product_detail'),
]
