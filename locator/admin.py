from django.contrib import admin
from locator.models import Category, Product, Brand

admin.site.site_header = 'Shoppstar'

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
