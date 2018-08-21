import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
from django.urls import reverse


class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(disabled=False)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)

    # add tag field for adding keywords related to category
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    objects = models.Manager()
    published = CategoryManager()
    disabled = models.BooleanField(default=False, blank=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locator:category_products', kwargs={'slug': self.slug})


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    is_company = models.NullBooleanField(default=True, null=True, blank=True)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=255, blank=True, null=True)

    # add tag field for adding keywords related to category
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    class Meta:
        db_table = 'brand'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Brand, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locator:brands', kwargs={'slug': self.slug})


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    sku = models.CharField(max_length=128)
    description = models.TextField()
    meta_description = models.TextField(default=" ")
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    store_url = models.URLField(default="")
    slug = models.SlugField(default="", blank=True,
                            unique=True, max_length=128)
    images = ArrayField(
        models.URLField(max_length=255),
        size=10,
        max_length=(255 * 11)  # 6 * 10 character nominals, plus commas
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    discount = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2, null=True)
    sender = models.CharField(default="", blank=True, max_length=128)
    brand = models.ForeignKey(
        Brand, related_name='brand', on_delete=models.CASCADE)
    collection = models.ForeignKey(
        Brand, related_name='collections', on_delete=models.SET_NULL, null=True)

    # add tag field for adding keywords related to product
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.meta_description = self.description[:30] + "..."
        self.slug = f'{slugify(self.name)}-{self.id.__hash__()%100000}'

        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locator:product_detail', kwargs={'slug': self.category.slug, 'pslug': self.slug})


class CollectionQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_published=True)

class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128)
    products = models.ManyToManyField(
        Product, blank=True, related_name='collections')
    image = models.URLField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    objects = CollectionQuerySet.as_manager()

    class Meta:
        ordering = ['pk']
        db_table = 'collection'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'locator:collection',
            kwargs={'slug': self.slug})