from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart , CartItem
from django.http import HttpResponse
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
    try:

        cart = Cart.objects.get(cart_id =_cart_id(request))  #for cart id we made  another function _cart_id above which is  fetching session id.
    except Cart.DoesNotExist:

        cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product , cart=cart)
        cart_item.quantity +=1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product =product,
            quantity =1, 
            cart=cart,
        )
        cart_item.save()
    
    return redirect('cart')

#  it is is handing the "-(minus)" button on cart page and deleting the quantity by one on every click
def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product= get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# It is handling remove button and removing the product itself along with its quantity on single click
def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product= get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


#  cart func is adding products to cart
# it also adding  each product to give total price of products inside the cart to us.
def cart(request,total=0,quantity=0,cart_items=None):

    try:
        cart= Cart.objects.get(cart_id =_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_available=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax


    except ObjectNotExist:
        pass #just ignores

    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total' : grand_total,

    }
    return render(request, 'store/cart.html',context)
