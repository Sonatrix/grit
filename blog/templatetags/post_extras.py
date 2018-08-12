from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag("blog/tags/latest_posts.html")
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by("-publish")[:count]
	return {"latest_posts": latest_posts}

@register.inclusion_tag("blog/tags/featured_posts.html")
def show_featured_posts(count=5):
	featured_posts = Post.published.exclude(is_featured=False).order_by("-publish")[:count]
	return {"featured_posts": featured_posts}
