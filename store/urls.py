from django.urls import path
from .views import homepage, productpage, orderspage, cartpage, salepage, topsellingpage, supplypage

urlpatterns = [
    path('', homepage, name='homepage'), 
    path('product/<id>', productpage, name='productpage'),
    path('order', orderspage, name='orderspage'),
    path('cart', cartpage, name='cartpage'),  
    path('supply', supplypage, name='supplypage'),  
    path('sale', salepage, name='salepage'),  
    path('top-selling', topsellingpage, name='topsellingpage'),  
]
