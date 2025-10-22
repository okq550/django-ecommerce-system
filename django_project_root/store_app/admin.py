from django.contrib import admin

from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    list_display = (
        "name",
        "slug",
        "price",
        "stock",
        "category",
        "created_at",
        "updated_at",
        "is_available",
    )


# Register your models here.
admin.site.register(Product, ProductAdmin)
