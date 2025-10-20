from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload='photos/categories', blank=True)