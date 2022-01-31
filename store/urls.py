from django.urls import path
from .views import IndexPage, ShopPage, productpage, OrdersPage, CartPage, CheckoutPage,\
                    WishlistPage, wishlistProduct, submit_review

urlpatterns = [
    path('', IndexPage.as_view(), name='homepage'), 
    path('shop', ShopPage.as_view(), name='shoppage'), 
    path('product/<id>', productpage, name='productpage'),
    path('submit_review/<id>', submit_review, name='submit_review'),
    path('order', OrdersPage.as_view(), name='orderspage'),
    path('cart', CartPage.as_view(), name='cartpage'),  
    path('checkout', CheckoutPage.as_view(), name='checkoutpage'), 
    path('wishlist', WishlistPage.as_view(), name='wishlistpage'),
    path('addtowishlist/<id>', wishlistProduct, name='product_wishlist')
]
