import feedparser
import requests

from time import mktime
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup 
from django.utils.text import slugify
from django.core.management.base import BaseCommand

from blog.models import Post
from locator.models import Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = ''
    help = 'Fetch list of blogs from rss feed'

    def handle(self, **options):

        feed = feedparser.parse('http://indiafashionblogger.com/feed/')

        for post in Post.objects.all():
            post.delete()

        loop_max = len(feed['entries'])
        category = Category.objects.get(id="ce867a33-fddf-4e60-89ec-179c9792889d")
        author = User.objects.get(pk=1)

        for i in range(0, loop_max):
            if feed['entries'][i]:
                blog_post = Post()
                blog_post.title = feed['entries'][i].title
                blog_post.slug = slugify(feed['entries'][i].title)
                link = self.parse_url(feed['entries'][i].link)
                blog_post.external_url = link
                blog_post.category = category
                blog_post.sender = "indiafashionblogger"
                blog_post.author = author
                blog_post.short_description = feed['entries'][i].description
                blog_post.body = self.get_content(link)
                blog_post.created = datetime.fromtimestamp(
                   mktime(feed['entries'][i].published_parsed))
                # print(blog_post.short_description)
                blog_post.save()

    def get_content(self, url):
        print("requesting url {}".format(url))
        response = requests.get(url)
        content = BeautifulSoup(response.content, "lxml")
        return repr(content.find(class_="content-main"))

    def parse_url(self, url):
        result = urlparse(url)
        print("url", result)
        return "".join(["https://", result.netloc, result.path])
# */30 * * * * /usr/bin/python3 /home/manage.py get_post 5
