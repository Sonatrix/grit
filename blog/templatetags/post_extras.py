from django import template
from blog.models import Post
from locator.models import Category

register = template.Library()


@register.inclusion_tag("blog/tags/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.inclusion_tag("blog/tags/featured_posts.html")
def show_featured_posts(count=5):
    featured_posts = Post.published.filter(
        is_featured=True).order_by("-publish")[:count]
    return {"featured_posts": featured_posts}

@register.inclusion_tag("blog/tags/post_item.html")
def top_posts(id=None):
    top_posts = Post.published.exclude(is_top=False).filter(
        category=id).order_by("-publish")[:3]
    return {"posts": top_posts}

@register.inclusion_tag("blog/tags/post_item.html")
def featured_posts(id=None):
    posts = Post.published.exclude(is_featured=False).filter(
        category=id).order_by("-publish")[:3]
    return {"posts": posts}

@register.inclusion_tag("blog/tags/post_item.html")
def latest_posts(id=None):
    posts = Post.published.filter(
        category=id).order_by("-publish")[:3]
    return {"posts": posts}

@register.inclusion_tag("blog/components/category_section.html")
def show_posts_by_category(id=None):
    featured_posts = Post.published.filter(
        category=id).order_by("-publish")[:4]
    category = Category.published.get(id=id)
    return {"featured_posts_by_category": featured_posts, "category": category}


@register.inclusion_tag("blog/components/post_banner.html")
def banner_posts(count=9):
    featured_posts = Post.published.exclude(
        is_featured=False).prefetch_related().order_by("-publish")
    left_section = featured_posts[:2]
    right_section = featured_posts[2:4]
    carousel_section = featured_posts[5:count]
    active_item = featured_posts[4]
    count = len(carousel_section)
    return {"left_section": left_section, "right_section": right_section, "carousel_section": carousel_section, "active_item": active_item, "count": count + 1}

@register.simple_tag
def humanizeTimeDiff(timestamp=None):
    """
    Returns a humanized string representing time difference
    between now() and the input timestamp.

    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """
    from datetime import datetime, timezone
    print(timestamp)
    timeDiff = datetime.now(timezone.utc) - timestamp
    days = int(timeDiff.days)
    hours = int(timeDiff.seconds / 3600)
    minutes = int(timeDiff.seconds % 3600 / 60)
    seconds = int(timeDiff.seconds % 3600 % 60)

    str = ""
    tStr = ""
    if days > 0:
        if days == 1:
            tStr = "day ago"
        else:
            tStr = "days ago"
        str = str + "%s %s" % (days, tStr)
        return str
    elif hours > 0:
        if hours == 1:
            tStr = "hour ago"
        else:
            tStr = "hours ago"
        str = str + "%s %s" % (hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:
            tStr = "min ago"
        else:
            tStr = "mins ago"
        str = str + "%s %s" % (minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:
            tStr = "sec ago"
        else:
            tStr = "secs ago"
        str = str + "%s %s" % (seconds, tStr)
        return str
    else:
        return None
