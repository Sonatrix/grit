# Generated by Django 2.1 on 2018-08-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0007_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='disabled',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
