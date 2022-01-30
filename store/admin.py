from django.contrib import admin
from .models import Product, ImageAlbum, CanvasSize, Order, Wishlist

# Register your models here.
admin.site.register(Product)
admin.site.register(ImageAlbum)
admin.site.register(CanvasSize)
admin.site.register(Order)
admin.site.register(Wishlist)
