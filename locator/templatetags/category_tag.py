from django import template
from locator.models import Category, Brand
from blog.models import Post

register = template.Library()


@register.inclusion_tag("locator/common/category_nav.html")
def show_categories():
    categories = Category.published.all().filter(parent=None)
    return {"categories": categories}

@register.inclusion_tag("locator/brands/brand_list.html")
def show_brands():
    brands = Brand.objects.all().exclude(image=None)[:5]
    return {"brands": brands}

@register.inclusion_tag("locator/common/category_footer.html")
def list_categories():
    categories = Category.published.all().filter(parent=None)
    return {"categories": categories}

@register.inclusion_tag("locator/tags/blog_section.html")
def top_posts_locator(count=3):
    top_posts = Post.published.prefetch_related().exclude(is_top=False).order_by("-publish")[:count]
    return {"posts": top_posts}