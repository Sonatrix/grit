from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')
		
class Post(models.Model):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'))
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	tags = ArrayField(models.CharField(max_length=250), blank=True, null=True)

	objects = models.Manager()
	published = PublishedManager()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	# need to add external url and images link
	category = models.ForeignKey('locator.Category', on_delete=models.CASCADE)

	class Meta:
		ordering = ('-publish',)
		db_table = 'post'

	def __str__(self):
		return self.title
    
	def get_absolute_url(self):
		return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

