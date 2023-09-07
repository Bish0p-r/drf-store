from django.db import models
from versatileimagefield.fields import VersatileImageField

from api.abstract.models import AbstractModel


class Product(AbstractModel):
    SEX_CHOICES = (
        ('M', 'Mens'),
        ('W', 'Womens'),
        ('U', 'Unisex'),
    )

    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    image = VersatileImageField(null=True, blank=True, upload_to='products_images')
    slug = models.SlugField(max_length=130, unique=True, db_index=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='U')

    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    brands = models.ManyToManyField('Brand', related_name='brand')

    @property
    def avg_rating(self):
        if self.total_reviews:
            return sum(i.rating for i in self.reviews.all()) / self.total_reviews
        return 0

    @property
    def total_reviews(self):
        return len(self.reviews.all())

    @property
    def is_available(self):
        return self.sizes.filter(quantity__gt=0).exists()

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=130, unique=True, db_index=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=130, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Size(AbstractModel):
    name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='sizes')

    def __str__(self):
        return f'{self.product} - {self.name}'


class Gallery(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    image = VersatileImageField(upload_to='gallery', blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='gallery')

    def __str__(self):
        return self.image.url
