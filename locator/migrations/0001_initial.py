# Generated by Django 2.0.7 on 2018-07-28 19:16

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('meta_description', models.TextField(default=' ')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('old_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('storeUrl', models.URLField(default='')),
                ('slug', models.SlugField(blank=True, default='', max_length=128, unique=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=255), max_length=2805, size=10)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('sender', models.CharField(blank=True, default='', max_length=128)),
                ('brand', models.CharField(blank=True, default='', max_length=128)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='locator.Category')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
