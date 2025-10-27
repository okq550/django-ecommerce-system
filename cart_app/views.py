from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect, render

from store_app.models import Product

from .models import Cart, CartItem

# Create your views here.


# Private function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def index(request):
    return render(request, "cart_app/index.html", {})


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # Get the cart using the _cart_id present in the session.
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quanity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect("cart_app:index")


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(
        request,
        "store/cart.html",
        {"total": total, "quantity": quantity, "cart_items": cart_item},
    )
