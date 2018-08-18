from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.text import slugify
from datetime import datetime

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    body = models.TextField()
    short_description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    external_url = models.URLField(default="", blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()
    is_featured = models.NullBooleanField(default=True, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    category = models.ForeignKey('locator.Category', on_delete=models.CASCADE)

    images = ArrayField(
        models.URLField(max_length=255, blank=True, null=True),
        size=10, blank=True, null=True,
        max_length=(255 * 11)  # 6 * 10 character nominals, plus commas
    )
    sender = models.CharField(max_length=255, default="shoppstar")

    class Meta:
        ordering = ('-publish',)
        db_table = 'post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
