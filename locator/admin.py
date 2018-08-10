from django.contrib import admin
from locator.models import Category, Product, Brand

admin.site.site_header = 'Shoppstar'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'description')

	list_filter = ('name',)
	search_fields = ('name', 'description', 'tags')
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'price','sender', 'category','created_at', 'meta_description', 'store_url')

	list_filter = ('brand', 'created_at', 'is_featured', 'category', 'sender',)
	search_fields = ('brand', 'description', 'tags', 'category',)
	prepopulated_fields = {'slug': ('name','brand',)}
	raw_id_fields = ('category','brand',)
	date_hierarchy = 'created_at'
	ordering = ('price', 'brand', 'is_featured')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'description')

	list_filter = ('name',)
	search_fields = ('name', 'description', 'tags')
	prepopulated_fields = {'slug': ('name',)}
