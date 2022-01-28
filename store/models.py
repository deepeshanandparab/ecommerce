from itertools import product
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from account.views import profile


ART_TYPE_CHOICES = (
    ('painting','painting'),
    ('antique','antique'),
    ('craft','craft'),
    ('furniture','furniture')
)

ART_CATEGORY_CHOICES = (
    ('sketch', 'sketch'),
    ('canvas painting','canvas painting'),
    ('abstract','abstract'),
    ('coins', 'coins'),
    ('rare item', 'rare item'),
    ('paper craft', 'paper craft'),
    ('wooden craft', 'wooden craft'),
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