import uuid
from django.db import models
from django_mysql.models import ListCharField

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, decimal_places=2)
    old_price = models.DecimalField(default=0.00, decimal_places=2)
    storeUrl = models.URLField(default="")
    images = ListCharField(
        base_field=models.URLField(max_length=200),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )

    storeUrl = models.URLField(default="")
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.BooleanField(default=False)

