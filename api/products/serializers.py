from rest_framework import serializers
from api.products.models import Product, Brand, ProductCategory, Size, Gallery


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ('product',)


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    # brands = BrandSerializer(many=True)
    brands = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    category = ProductCategorySerializer()
    sizes = SizeSerializer(many=True)
    gallery = GallerySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'article',
            'description', 'created', 'image',  'slug',
            'sex', 'category', 'brands', 'sizes', 'gallery'
                  )
