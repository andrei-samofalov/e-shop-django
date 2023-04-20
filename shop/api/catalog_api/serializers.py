import datetime

from rest_framework import serializers

from catalog.models import Category, Product, ProductOffer, Review, Tag


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = 'id', 'product'
        optional_fields = ('product_id',)

    product_id = serializers.IntegerField(source='product.id')
    date = serializers.SerializerMethodField('get_date')

    @classmethod
    def get_date(cls, obj: Review):
        return datetime.datetime.strftime(obj.date, '%Y-%m-%d %H:%M')

    def create(self, validated_data):
        product_id = validated_data.pop('product')['id']
        return Review.objects.create(product_id=product_id, **validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name'


class ProductSerializer(serializers.ModelSerializer):
    """
    usages:
      api/products/{id}
    """

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'categoryName',
            'price',
            'stock',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'href',
            'freeDelivery',
            'rating',
            'images',
            'tags',
            'reviews',
            'specifications',
        )
        optional_fields = ('category', 'count')
        depth = 1

    rating = serializers.FloatField()
    categoryName = serializers.CharField(source='category.title')
    category = serializers.IntegerField(source='category.id')
    images = serializers.SerializerMethodField('get_images')
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    @classmethod
    def get_images(cls, obj: Product):
        return [i.image.url for i in obj.images.all()]


class ProductShortSerializer(ProductSerializer):
    """
    ---
    usages:
      api/orders [all]
      api/basket [get]
      api/banners
      api/products/limited
      api/products/popular
      api/catalog
      api/catalog/{id}
    """

    class Meta(ProductSerializer.Meta):
        optional_fields = ('tags',)

    reviews = serializers.SerializerMethodField('get_reviews_amount')

    @classmethod
    def get_reviews_amount(cls, obj: Product):
        return obj.reviews.count()


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOffer
        fields = (
            'id',
            'price',
            'salePrice',
            'dateFrom',
            'dateTo',
            'title',
            'href',
            'images',
        )

    id = serializers.IntegerField(source='product.id')
    price = serializers.DecimalField(
        source='product.price', decimal_places=2, max_digits=10
    )
    title = serializers.CharField(source='product.title')
    href = serializers.CharField(source='product.href')
    images = serializers.SerializerMethodField('get_product_images')

    @classmethod
    def get_product_images(cls, obj: ProductOffer):
        return [i.image.url for i in obj.product.images.all()]


class CategoryCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'image',
            'href',
        )


class CategorySerializer(CategoryCommonSerializer):
    class Meta(CategoryCommonSerializer.Meta):
        # how to inherit in case of DRY?
        fields = (
            'id',
            'title',
            'image',
            'href',
            'subcategories',
        )
        depth = 1

    subcategories = CategoryCommonSerializer(many=True)
