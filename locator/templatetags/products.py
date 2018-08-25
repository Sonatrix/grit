from django import template
from locator.models import Category, Product, Collection

register = template.Library()

@register.inclusion_tag("locator/tags/category_item_section.html")
def show_products(id=None, count=10):
    category = Category.objects.select_related().get(id=id)
    products = None

    if category.parent_id is not None:
        products = Product.objects.prefetch_related().filter(category_id=category.id)[:count]

    else:
        category_ids = Category.objects.all().filter(
            id=category.id).values_list("children__id", flat=True).distinct()
        products = Product.objects.prefetch_related().filter(category__in=category_ids).order_by('?')[:count]

    return {"products": products, "category": category}

@register.inclusion_tag("locator/tags/collection.html")
def show_collections(count=3):
	collections = Collection.published.all()[:count]

	return {"collections": collections}

@register.inclusion_tag("locator/tags/collection_item.html")
def collection_item(id=None, count=10):
    collection = Collection.published.get(id=id)
    products = collection.get_products()[:count]
    return {"products": products, "collection": collection}