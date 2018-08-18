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

@register.inclusion_tag("blog/components/post_banner.html")
def banner_posts(count=9):
	featured_posts = Post.published.exclude(is_featured=False).prefetch_related().order_by("-publish")
	left_section = featured_posts[:2]
	right_section = featured_posts[2:4]
	carousel_section = featured_posts[5:count]
	active_item = featured_posts[4]
	count = len(carousel_section)
	return {"left_section": left_section, "right_section": right_section, "carousel_section": carousel_section, "active_item": active_item, "count": count+1}
