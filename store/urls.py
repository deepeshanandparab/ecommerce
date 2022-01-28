from django.urls import path
from .views import HomePage, productpage, orderspage, CartPage, CheckoutPage, salepage, topsellingpage, supplypage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'), 
    path('product/<id>', productpage, name='productpage'),
    path('order', orderspage, name='orderspage'),
    path('cart', CartPage.as_view(), name='cartpage'),  
    path('checkout', CheckoutPage.as_view(), name='checkoutpage'), 
    path('supply', supplypage, name='supplypage'),  
    path('sale', salepage, name='salepage'),  
    path('top-selling', topsellingpage, name='topsellingpage'),  
]
