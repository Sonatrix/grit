# Generated by Django 2.0.6 on 2018-07-01 17:45

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=django_mysql.models.ListCharField(models.URLField(max_length=255), max_length=2805, size=10),
        ),
    ]