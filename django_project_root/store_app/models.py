from django.db import models
from django.urls import reverse

from django_project_root.category_app.models import Category


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=5,
    )
    image = models.ImageField(upload_to="photos/products", blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse("store_app:product_detail", args=[self.category.slug, self.slug])
