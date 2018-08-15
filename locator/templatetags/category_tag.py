from django import template
from locator.models import Category, Brand

register = template.Library()


@register.inclusion_tag("locator/common/category_nav.html")
def show_categories():
    categories = Category.published.all().filter(parent=None)
    return {"categories": categories}

@register.inclusion_tag("locator/brands/brand_list.html")
def show_brands():
    brands = Brand.objects.all().exclude(image=None)[:5]
    return {"brands": brands}