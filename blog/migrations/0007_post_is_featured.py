# Generated by Django 2.1 on 2018-08-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.NullBooleanField(default=True),
        ),
    ]
