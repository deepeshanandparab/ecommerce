from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Order, Wishlist
from django.contrib.auth.models import User
from .filters import ProductSearch
from django.views import View

class HomePage(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print('cart', cart)
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        
        return redirect('homepage')


    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        keyword = request.GET.get('name')
        if keyword != None:
            product_list = Product.objects.filter(name__contains=keyword, approved=True).order_by('-created_at')
        else:
            product_list = Product.objects.filter(name__contains='', approved=True).order_by('-created_at')

        paginator = Paginator(product_list, 8)
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        first_item_number = 8 * (response.number - 1) + 1 

        context = {
                    'title': 'Home',
                    'search_filter': product_list,
                    'products_list': response,
                    'page_size': 8,
                    'page_number': page,
                    'first_item_number': first_item_number,
                    'search_keyword': keyword}
        return render(request, 'home.html', context)



def productpage(request, id):
    products_list = Product.objects.filter(id=id)

    if products_list[0].wishlist.filter(id=request.user.id).exists():
        is_wishlisted = True
    else:
        is_wishlisted = False

    context = {'title': 'Product', 'products_list': products_list, 'is_wishlisted': is_wishlisted}
    return render(request, 'product.html', context)    
  

class CartPage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart        
        return redirect('cartpage')


    def get(self, request):
        ids = list(request.session.get('cart').keys())
        cart_list = Product.get_products_by_id(ids) 
        return render(request, 'cart.html', {'cart_list':cart_list})   


class CheckoutPage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        username = request.session.get('username')
        first_name = request.POST.get('order_first_name')
        last_name = request.POST.get('order_last_name')
        email = request.POST.get('order_email')
        addr1 = request.POST.get('order_addr1')
        addr2 = request.POST.get('order_addr2')
        pincode = request.POST.get('order_pincode')
        country = request.POST.get('order_country')
        del_method = request.POST.get('order_del_method')
        contact = request.POST.get('order_contact')
        alternate_contact = request.POST.get('order_alternate_contact')
        terms = request.POST.get('order_terms')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        
        for product in products:
            order = Order(
                product = product,
                user = request.user,
                quantity = cart.get(str(product.id)),
                price = product.price,
                first_name = first_name,
                last_name = last_name,
                email = email,
                addr1 = addr1,
                addr2 = addr2,
                pincode = pincode,
                country = country,
                delivery_method = del_method,
                contact = contact,
                alt_contact = alternate_contact,
                terms = terms
            )
            order.save()
            request.session['cart'] = {}
        return redirect('orderspage')


    def get(self, request):
        ids = list(request.session.get('cart').keys())
        cart_list = Product.get_products_by_id(ids)
        return render(request, 'checkout.html', {'cart_list':cart_list})



class OrdersPage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    
    def post(self, request):
        pass


    def get(self, request):
        order_list = Order.objects.filter(user=request.user).order_by('-date')
        return render(request, 'orders.html', {'order_list':order_list})



class WishlistPage(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'

    
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        if product.wishlist.filter(id=request.user.id).exists():
            product.wishlist.remove(request.user)
            Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
        return redirect('wishlistpage')


    def get(self, request):
        product = Product.objects.all()
        wishlist = []
        for p in product:
            if p.wishlist.filter(id=request.user.id).exists():
                wishlist.append(p)
        return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required
def wishlistProduct(request, id):
    product = Product.objects.get(id=id)
    is_wishlist = False
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        Wishlist.objects.filter(product_id=product, user_id=request.user).delete()
        is_wishlist = False
    else:
        product.wishlist.add(request.user)
        Wishlist.objects.create(product_id=product, user_id=request.user)
        is_wishlist = True
    return redirect('productpage', id)


def supplypage(request):
    return render(request, 'supply.html')


def salepage(request):
    return render(request, 'sale.html')  


def topsellingpage(request):
    return render(request, 'top_selling.html')  


