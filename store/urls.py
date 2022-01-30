from django.urls import path
from .views import HomePage, productpage, OrdersPage, CartPage, CheckoutPage,\
                    WishlistPage, wishlistProduct, salepage, topsellingpage, supplypage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'), 
    path('product/<id>', productpage, name='productpage'),
    path('order', OrdersPage.as_view(), name='orderspage'),
    path('cart', CartPage.as_view(), name='cartpage'),  
    path('checkout', CheckoutPage.as_view(), name='checkoutpage'), 
    path('wishlist', WishlistPage.as_view(), name='wishlistpage'),
    path('addtowishlist/<id>', wishlistProduct, name='product_wishlist'),
    path('supply', supplypage, name='supplypage'),  
    path('sale', salepage, name='salepage'),  
    path('top-selling', topsellingpage, name='topsellingpage'),  
]
