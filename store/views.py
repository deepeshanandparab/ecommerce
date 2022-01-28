from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product
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
        print('cart', cart)      
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



# # Create your views here.
# def homepage(request):
#     keyword = request.GET.get('name')
#     if keyword != None:
#         product_list = Product.objects.filter(name__contains=keyword, approved=True).order_by('-created_at')
#     else:
#         product_list = Product.objects.filter(name__contains='', approved=True).order_by('-created_at')

#     paginator = Paginator(product_list, 4)
#     page = request.GET.get('page')
#     try:
#         response = paginator.page(page)
#     except PageNotAnInteger:
#         response = paginator.page(1)
#     except EmptyPage:
#         response = paginator.page(paginator.num_pages)

#     first_item_number = 4 * (response.number - 1) + 1

#     context = {
#                 'title': 'Home',
#                 'search_filter': product_list,
#                 'products_list': response,
#                 'page_size': 4,
#                 'first_item_number': first_item_number,
#                 'search_keyword': keyword}
#     return render(request, 'home.html', context)


def productpage(request, id):
    products_list = Product.objects.filter(id=id)
    context = {'title': 'Product', 'products_list': products_list}
    return render(request, 'product.html', context)    


def orderspage(request):
    return render(request, 'orders.html')   


class CartPage(View):

    def get(self, request):
        ids = list(request.session.get('cart').keys())
        cart_list = Product.get_products_by_id(ids) 
        return render(request, 'cart.html', {'cart_list':cart_list})   


def supplypage(request):
    return render(request, 'supply.html')


def salepage(request):
    return render(request, 'sale.html')  


def topsellingpage(request):
    return render(request, 'top_selling.html')  


