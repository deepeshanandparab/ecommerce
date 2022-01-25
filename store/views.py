from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product
from .filters import ProductSearch


# Create your views here.
def homepage(request):
    keyword = request.GET.get('name')
    if keyword != None:
        product_list = Product.objects.filter(name__contains=keyword).order_by('-created_at')
    else:
        product_list = Product.objects.filter(name__contains='').order_by('-created_at')

    paginator = Paginator(product_list, 4)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    first_item_number = 4 * (response.number - 1) + 1

    context = {
                'title': 'Home',
                'search_filter': product_list,
                'products_list': response,
                'page_size': 4,
                'first_item_number': first_item_number,
                'search_keyword': keyword}
    return render(request, 'home.html', context)


def productpage(request, id):
    products_list = Product.objects.filter(id=id)
    context = {'title': 'Product', 'products_list': products_list}
    return render(request, 'product.html', context)    


def orderspage(request):
    return render(request, 'orders.html')   


def cartpage(request):
    return render(request, 'cart.html')   


def supplypage(request):
    return render(request, 'supply.html')


def salepage(request):
    return render(request, 'sale.html')  


def topsellingpage(request):
    return render(request, 'top_selling.html')  


