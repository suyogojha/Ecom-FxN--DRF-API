from carts.models import CartItem, Cart
from carts.views import _cart_id

# custom context processor to show cart item count in navbar
def counter(request): 
    cart_count = 0
    if 'admin' in request.path: # to avoid showing cart item count in admin panel
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1]) # get the cart items associated with the cart
            for cart_item in cart_items:
                cart_count += cart_item.quantity # count the total quantity of items in the cart
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count) 