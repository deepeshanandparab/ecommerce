from django.urls import path
from .views import HomePage, productpage, orderspage, CartPage, salepage, topsellingpage, supplypage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'), 
    path('product/<id>', productpage, name='productpage'),
    path('order', orderspage, name='orderspage'),
    path('cart', CartPage.as_view(), name='cartpage'),  
    path('supply', supplypage, name='supplypage'),  
    path('sale', salepage, name='salepage'),  
    path('top-selling', topsellingpage, name='topsellingpage'),  
]
