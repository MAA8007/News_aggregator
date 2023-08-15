from django.db import models
from datetime import datetime


class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    category = models.CharField(max_length=20)
    website = models.CharField(max_length=200, default='some_default_value')
    published = models.DateTimeField(default=datetime.now)
    image = models.URLField(default=None)