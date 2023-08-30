from django.db import models

from api.abstract.models import AbstractModel


class Product(AbstractModel):
    name = models.CharField(max_length=256)
    brands = models.ManyToManyField('Brand', related_name='brand')
    description = models.TextField(blank=True)
    article = models.CharField(max_length=128, null=True, blank=True, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=130, unique=True, db_index=True)
    sex = models.CharField(max_length=10, choices=(
        ('M', 'Mens'),
        ('W', 'Womens'),
        ('U', 'Unisex'),
    ),
        default='U')

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
    image = models.ImageField(upload_to='gallery')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
