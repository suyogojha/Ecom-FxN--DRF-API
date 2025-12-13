from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# Helper function to get the cart ID
def _cart_id(request):
    cart = request.session.session_key # get the session key
    if not cart:
        cart = request.session.create() # create a new session if not present
    return cart

# View to add a product to the cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product
    product_variation = []
    if request.method == 'POST':
        for item  in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(card_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            card_id=_cart_id(request) # create a new cart if not present
        )
        cart.save()
    # Add or update the cart item
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() 
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart,) # get the cart item if the product is already in the cart
        #existing_variation -> database
        # current_variation -> product_variation
        # item id -> database
        
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
            # increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

 
# View to display the cart
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(card_id=_cart_id(request)) # get the cart using the cart_id present in the session
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get the cart items associated with the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # calculate the total price
            quantity += cart_item.quantity # calculate the total quantity
        tax = (2 * total) / 100 # calculate tax as 2% of total
        grand_total = total + tax # calculate grand total
    except ObjectDoesNotExist: # type: ignore
        pass  # ignore if cart does not exist
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


# View to remove a product from the cart (-)
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(card_id=_cart_id(request)) # get the cart using the cart_id present in the session
    product = get_object_or_404(Product, id=product_id) # get the product
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cart item associated with the product and cart
        if cart_item.quantity > 1:
            cart_item.quantity -= 1 # decrease the quantity
            cart_item.save() # save the cart item
        else:
            cart_item.delete() # delete the cart item if quantity is 1
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(card_id=_cart_id(request)) # get the cart using the cart_id present in the session
    product = get_object_or_404(Product, id=product_id) # get the product
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cart item associated with the product and cart
    cart_item.delete() # delete the cart item
    return redirect('cart')