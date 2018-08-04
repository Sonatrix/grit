from django.contrib import admin
from locator.models import Category, Product

admin.site.site_header = 'Shoppstar'

admin.site.register(Category)
admin.site.register(Product)
