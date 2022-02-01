from itertools import product
from operator import mod
from select import select
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
import datetime
from account.views import profile


ART_TYPE_CHOICES = (
    ('painting','painting'),
    ('antique','antique'),
    ('craft','craft'),
    ('furniture','furniture')
)

ART_CATEGORY_CHOICES = (
    ('sketch', 'sketch'),
    ('canvas_painting','canvas_painting'),
    ('abstract','abstract'),
    ('coins', 'coins'),
    ('rare_item', 'rare_item'),
    ('paper_craft', 'paper_craft'),
    ('wooden_craft', 'wooden_craft'),
    ('chair', 'chair'),
    ('chandelier', 'chandelier'),
    ('closet', 'closet'),
    ('table', 'table')
)

CANVAS_SIZE_CHOICES = (
    ('3x4','3x4'),
    ('6x8','6x8'),
    ('12x16','12x16'),
    ('24x32','24x32')
)

ORDER_STATUS_CHOICES = (
    ('pending','pending'),
    ('complete','complete')
)


def get_upload_path(instance, filename):
    model = getattr(instance, 'name')
    album_name = model.replace(' ', '_')
    return f'{album_name}/images/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField()
    discounted_price = models.IntegerField(null=True, blank=True)
    art_type = models.CharField(max_length=15, choices=ART_TYPE_CHOICES, default='', null=True, blank=True)
    art_category = models.CharField(max_length=50, choices=ART_CATEGORY_CHOICES, default='Others')
    description = models.CharField(max_length=500)
    original_art_by = models.CharField(max_length=20)
    artist = models.ForeignKey(User, related_name='artist', on_delete=models.CASCADE)
    sold_by = models.CharField(max_length=20)
    approved = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)
    

    def save_discounted_price(self, price, discount):
        self.discounted_price =  price * (1-discount/100)
        self.save()


    def __str__(self):
        return self.name


class CanvasSize(models.Model):
    product = models.ForeignKey(Product, related_name='canvas_product', on_delete=models.CASCADE)
    canvas_size = models.CharField(max_length=50, choices=CANVAS_SIZE_CHOICES, default='')
    in_stock = models.BooleanField(default=True)
    quantity_available = models.IntegerField()
    quantity_sold = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.get_canvas_size_display()} canvas size'


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to=get_upload_path)
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)

    def default(self):
        return self.images.filter(default=True).first()

    def thumbnails(self):
        return self.images.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=30, default='')
    addr1 = models.TextField(max_length=100, default='')
    addr2 = models.TextField(max_length=100, default='')
    pincode = models.CharField(max_length=10, default='')
    country = models.CharField(max_length=20, default='')
    delivery_method = models.CharField(max_length=10, default='standard')
    contact = models.CharField(max_length=10, default='')
    alt_contact = models.CharField(max_length=10, null=True, blank=True)
    terms = models.CharField(max_length=10, default='accepted')
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order: {self.product.name}({self.quantity}) - {self.price} \
                        by {self.first_name} {self.last_name} {self.date}'


class Wishlist(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_product')
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='wishlist_user')

    def __str__(self):
        return f'{self.user_id} wishlisted product number : {self.product_id.name}'


class RatingReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating_product')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='rating_user')
    subject = models.CharField(max_length=20, null=True, blank=True)
    rating = models.FloatField()
    review = models.TextField(max_length=200, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user} rated {self.product.name} with {self.rating} stars'