from django.shortcuts import render

from django_project_root.category_app.models import Category
from django_project_root.store_app.models import Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    return render(
        request,
        "home_app/index.html",
        {
            "categories": categories,
            "products": products,
        },
    )
