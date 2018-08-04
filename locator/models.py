import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)

    # add tag field for adding keywords related to category
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

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
    store_url = models.URLField(default="")
    slug = models.SlugField(default="",blank=True, unique=True, max_length=128)
    images = ArrayField(
        models.URLField(max_length=255),
        size=10,
        max_length=(255 * 11)  # 6 * 10 character nominals, plus commas
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.NullBooleanField(default=False, null=True, blank=True)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, null=True)
    sender = models.CharField(default="",blank=True, max_length=128)
    brand = models.CharField(default="",blank=True, max_length=128)
    
    # add tag field for adding keywords related to product
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.meta_description = self.description[:30] + "..."
        self.slug = f'{slugify(self.name)}-{self.id[1:6]}'

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locator:product_detail', kwargs={'slug': self.category.slug, 'pslug': self.slug})




