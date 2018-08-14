from django import template
from locator.models import Category

register = template.Library()


@register.inclusion_tag("locator/common/category_nav.html")
def show_categories():
    categories = Category.published.all().filter(parent=None)
    return {"categories": categories}
