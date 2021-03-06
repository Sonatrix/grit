# Generated by Django 2.1 on 2018-08-19 16:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0011_auto_20180819_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128)),
                ('image', models.URLField(blank=True, max_length=255, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(blank=True, related_name='collections', to='locator.Product')),
            ],
            options={
                'db_table': 'collection',
                'ordering': ['pk'],
            },
        ),
    ]
