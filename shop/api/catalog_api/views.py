from django.db.models import Avg, Count, Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.catalog_api.filters import ProductFilter
from api.catalog_api.paginators import CatalogPaginator
from api.catalog_api.serializers import (
    CategorySerializer,
    OfferSerializer,
    ProductSerializer,
    ProductShortSerializer,
    ReviewSerializer,
    TagSerializer,
)
from catalog.models import Category, Product, ProductOffer, Review, Tag


class CachedListAPIView(ListAPIView):
    """Abstract ListAPIView-based class with cached get-route"""
    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetail(RetrieveAPIView):
    queryset = (
        Product.objects
        .filter(is_active=True)
        .prefetch_related(
            'reviews', 'tags', 'category', 'images', 'specifications'
        )
    )
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductListCommon(CachedListAPIView):
    """Abstract CachedListAPIView-based class"""
    serializer_class = ProductShortSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductListLimited(ProductListCommon):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_limited=True)[:16]


class ProductListBanners(ProductListCommon):
    def get_queryset(self):
        return super().get_queryset()[:4]


class ProductListPopular(ProductListCommon):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.alias(rating=Avg('reviews__rate')).order_by('-rating')[:8]


class ReviewCreate(CreateAPIView):
    serializer_class = ReviewSerializer
    product_id = None

    def get_queryset(self):
        return (
            Review.objects
            .select_related('product')
            .filter(product_id=self.product_id)
        )

    def create(self, request, *args, **kwargs):
        self.product_id = kwargs.get('pk')

        request.data.update({'product_id': self.product_id})
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        all_reviews = self.get_serializer(data=self.get_queryset(), many=True)
        all_reviews.is_valid()

        return Response(all_reviews.data, status=status.HTTP_201_CREATED)


class TagList(CachedListAPIView):
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer


class CatalogList(CachedListAPIView):
    pagination_class = CatalogPaginator
    serializer_class = ProductShortSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        qs = (
            Product.objects
            .filter(is_active=True)
            .annotate(_rating=Avg('reviews__rate'))
            .annotate(_purchases=Sum('purchases__quantity'))
            .annotate(_reviews=Count('reviews'))
        ).order_by('-_purchases')
        if tags := self.request.query_params.getlist('tags[]'):
            qs = qs.filter(tags__name__in=tags)

        return qs


class CategoryList(CachedListAPIView):
    queryset = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related('subcategories')
    )
    serializer_class = CategorySerializer


class OfferList(CachedListAPIView):
    queryset = (
        ProductOffer.objects
        .filter(is_active=True)
        .select_related('product')
    )
    serializer_class = OfferSerializer
