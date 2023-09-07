from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from api.products.models import Product, Brand,  Size, Gallery, ProductCategory
from api.reviews.serializers import ReviewSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('name',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('public_id', 'name', 'quantity',)


class GallerySerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='public_id', read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )

    class Meta:
        model = Gallery
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    brands = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    category = ProductCategorySerializer()
    sizes = SizeSerializer(many=True, read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'public_id', 'name', 'price',
            'description', 'created', 'image',  'slug',
            'sex', 'category', 'brands', 'sizes', 'gallery',
            'total_reviews', 'avg_rating', 'reviews',
                  )
