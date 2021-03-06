# Generated by Django 2.1 on 2018-08-19 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0010_auto_20180819_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_trending',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='locator.Category'),
        ),
    ]
