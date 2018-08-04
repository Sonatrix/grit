from django.contrib.sitemaps import Sitemap
from locator.models import Product, Category

class ProductSitemap(Sitemap):    
    changefreq = "daily"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at