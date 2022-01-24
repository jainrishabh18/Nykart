from django.shortcuts import render,get_object_or_404
from carts.views import _cart_id
from carts.models import CartItem
from .models import Product
# this is importing models of category app ,model name= Category
from category.models import Category
# imports for pagination
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
def store(request,category_slug=None):

    categories = None
    products = None
    # "if" below is handling pagination for categories ex if we go to shirts so it will show only 1 product per page.  
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        # below code is for pagination -> it is going from one page to another page with help of this code 
        #  fro detailed understanding of pagination go through pagination documentry on django
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        # above code is for pagination
        product_count =products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # BELOW LINE IS SAYING on every page maximun 6 product can be seen  and remaining products will be seen on another page
        paginator = Paginator(products,6)
        # requesting for page  using get method
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count =products.count()



    context={
        'products':paged_products,
        'product_count':product_count 
    }
    
    return render(request, 'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        # 1. we go in product model
        # 2. we find category there we want slug of that category
        # 3. we go to category model and took category slug from there 
        # 4. all the above work is done by "category__slug=category_slug"(double underscore in cat_slug went model to model to do that)
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # <!--  in_cart check wheather product is added to cart or not...exists() return true or false -->
        in_cart =CartItem.objects.filter(cart__cart_id =_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request, 'store/product_detail.html',context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count =products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html',context)