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
