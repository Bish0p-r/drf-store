from rest_framework import serializers
from api.products.models import Product, Brand, ProductCategory, Size, Gallery
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
    class Meta:
        model = Gallery
        fields = ('id', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    brands = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    category = ProductCategorySerializer()
    sizes = SizeSerializer(many=True)
    gallery = GallerySerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'public_id', 'name', 'price', 'article',
            'description', 'created', 'image',  'slug',
            'sex', 'category', 'brands', 'sizes', 'gallery',
            'total_reviews', 'avg_rating', 'reviews',
                  )
