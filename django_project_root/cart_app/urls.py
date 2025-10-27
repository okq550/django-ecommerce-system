from django.urls import path

from . import views

app_name = "cart_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
]
