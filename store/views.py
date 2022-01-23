from django.shortcuts import render
from .models import Product

# Create your views here.
def homepage(request):
    products_list = Product.objects.all()
    context = {'title': 'Home', 'products_list': products_list}
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


