from django.contrib import admin

from catalog.models import (
    Category,
    Product,
    ProductImage,
    ProductOffer,
    Review,
    Specification,
    Tag,
)
from common_mixins.admin_mixins import SoftDeleteMixin


@admin.register(Specification)
class SpecificationAdmin(SoftDeleteMixin, admin.ModelAdmin):
    pass


@admin.register(ProductOffer)
class ProductOfferAdmin(SoftDeleteMixin, admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(SoftDeleteMixin, admin.ModelAdmin):
    filter_horizontal = ('subcategories',)


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(SoftDeleteMixin, admin.ModelAdmin):
    inlines = [ProductImagesInline]
    list_display = ['title', 'stock', 'price']
    list_editable = ['price', 'stock']
    filter_horizontal = 'tags', 'specifications'
    exclude = ('count',)
    search_fields = ('title', 'fullDescription')
    list_filter = ('is_active', 'is_limited')


class ProductInline(admin.TabularInline):
    model = Product.tags.through
    extra = 1


@admin.register(Tag)
class TagAdmin(SoftDeleteMixin, admin.ModelAdmin):
    inlines = [ProductInline]
