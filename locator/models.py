import uuid
from django.db import models
from django_mysql.models import ListCharField
from django.utils.text import slugify

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    meta_description = models.TextField(default=" ")
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    old_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    storeUrl = models.URLField(default="")
    slug = models.SlugField(default="",blank=True, unique=True, max_length=128)
    images = ListCharField(
        base_field=models.URLField(max_length=255),
        size=10,
        max_length=(255 * 11)  # 6 * 10 character nominals, plus commas
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.BooleanField(default=False)
    sender = models.CharField(default="",blank=True, max_length=128)
    brand = models.CharField(default="",blank=True, max_length=128)
    
    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.meta_description = self.description[:30] + "..."
        self.slug = f'{slugify(self.name)}-{self.id[1:6]}'
        super(Product, self).save(*args, **kwargs)




