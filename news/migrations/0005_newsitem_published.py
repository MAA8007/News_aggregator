# Generated by Django 4.2.4 on 2023-08-13 07:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_newsitem_website_alter_newsitem_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='published',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]