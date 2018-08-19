# Generated by Django 2.1 on 2018-08-19 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0009_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_trending',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='locator.Category'),
        ),
    ]