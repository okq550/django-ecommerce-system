from django.urls import path

from . import views

app_name = "store_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:category_slug>/", views.index, name="products_by_category"),
    path(
        "<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
]
