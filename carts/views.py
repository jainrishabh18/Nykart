from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart , CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


#  The session framework lets you store and retrieve arbitrary data on a per-site-visitor basis. 
# It stores data on the server side and abstracts the sending and receiving of cookies.
#  Cookies contain a session ID – not the data itself (unless you’re using the cookie based backend).


# it is fetching cart_id using session keys
def _cart_id(request):
    
    # whenever we add a product to cart it will generate session id.
    # we get that session_id from cookies on server side
      
    # below code line is fetching session_id
    cart=request.session.session_key
    # if no cart then it is generating a cart using session
    if not cart:
        cart=request.session.create()
    return cart

#  add_cart  view is fetching product_id , cart_id and adding product to cart and saving it.

def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)  #getting product
    # 6lecupdate
    product_variation =[]
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation =Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                # 6lec update
                product_variation.append(variation)

                
            except:
                pass
    
    
    
    
    try:

        cart = Cart.objects.get(cart_id =_cart_id(request))  #for cart id we made  another function _cart_id above which is  fetching session id.
    except Cart.DoesNotExist:

        cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
    cart.save()


    is_cart_item_exists =CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product , cart=cart)
        # existing_variations -> database
        # current_variation ->product_variation
        # item_id = database
                
        # ex here is existing
        ex_var_list = []
        id=[]
        for item in cart_item:
            existing_variations = item.variations.all()
            ex_var_list.append(list(existing_variations))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
            # increase cart item quantity
            index = ex_var_list.index(product_variation)
            item_id =id[index]
            item =CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()

        else:
            item =CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
           

#if cart dont have any item then we will go to except and add 1st product to it
    else:
        cart_item = CartItem.objects.create(
            product =product,
            quantity =1, 
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    
    return redirect('cart')

#  it is is handing the "-(minus)" button on cart page and deleting the quantity by one on every click
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product= get_object_or_404(Product,id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# It is handling remove button and removing the product itself along with its quantity on single click
def remove_cart_item(request,product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product= get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


#  cart func is adding products to cart
# it also adding  each product to give total price of products inside the cart to us.
def cart(request,total=0,quantity=0,cart_items=None):

    try:
        tax=0
        grand_total=0

        cart= Cart.objects.get(cart_id =_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    # we have put 2 % tax on each product
        tax = (2 * total)/100
        grand_total = total + tax


    except ObjectDoesNotExist:
        pass #just ignores

    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total' : grand_total,

    }
    return render(request, 'store/cart.html',context)
