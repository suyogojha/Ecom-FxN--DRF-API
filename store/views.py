from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
# View to display products in the store
def store(request, category_slug=None):
    categories = None # to hold category object
    products = None # to hold product object

    if category_slug != None: # if category slug is present in the url
        categories = get_object_or_404(Category, slug=category_slug) # get the category object using the slug
        products = Product.objects.filter(category=categories, is_available=True) # filter products based on category and availability
        paginator = Paginator(products, 1) # show 1 product per page
        page = request.GET.get('page') # get the page number from the url
        paged_products = paginator.get_page(page) # get the products for the requested page
        product_count = products.count() # count the total number of products in the category
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') # get all available products ordered by id
        paginator = Paginator(products, 3) # show 3 products per page
        page = request.GET.get('page') # get the page number from the url
        paged_products = paginator.get_page(page) # get the products for the requested page
        product_count = products.count() # count the total number of products

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)



# View to display product detail page
def product_detail(request, category_slug, product_slug):
    try: 
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # get the product using category slug and product slug
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() # check if the product is already in the cart
    except Exception as e: # catch any exception
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)






def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            context = {
                'products': products,
                'product_count': product_count,
            }
            return render(request, 'store/store.html', context)
    return render(request, 'store/store.html')