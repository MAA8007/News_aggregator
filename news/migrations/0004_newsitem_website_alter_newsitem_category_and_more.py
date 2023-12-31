# Generated by Django 4.2.4 on 2023-08-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_newsitem_image_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='website',
            field=models.CharField(default='some_default_value', max_length=200),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='category',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
