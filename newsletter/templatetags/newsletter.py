from django import template

register = template.Library()

@register.inclusion_tag("newsletter/tags/newsletter.html")
def subscribe_newsletter(name="trending-products"):

    return {"name": name}