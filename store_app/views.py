from django.shortcuts import get_object_or_404, render

from category_app.models import Category

from .models import Product


def index(request, category_slug=None):
    categories = None
    products = None
    products_count = 0
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        categories = Category.objects.all()
        products = Product.objects.filter(is_available=True)

    products_count = products.count

    # print(f"category_slug: {category_slug}")
    # print(vars(categories))

    return render(
        request,
        "store_app/index.html",
        {
            "categories": categories,
            "products": products,
            "products_count": products_count,
        },
    )


def product_detail(request, category_slug, product_slug):
    try:
        # Get the product where the category__slug is applied to the relation category with the slug column.
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        # DoesNotExist exception
        raise e

    return render(
        request,
        "store_app/product_detail.html",
        {
            "single_product": single_product,
            # "categories": categories,
            # "products": products,
            # "products_count": products_count,
        },
    )
