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
    list_display = 'product_title', "dateFrom", 'dateTo'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


class SubcategoriesInline(admin.TabularInline):
    model = Category.subcategories.through
    fk_name = 'to_category'
    extra = 1
    verbose_name = _('parent category')
    verbose_name_plural = _('parent categories')


@admin.register(Category)
class CategoryAdmin(SoftDeleteMixin, admin.ModelAdmin):
    filter_horizontal = ('subcategories',)
    inlines = [SubcategoriesInline]


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
    prepopulated_fields = {"slug": ("title",)}


class ProductInline(admin.TabularInline):
    model = Product.tags.through
    extra = 1


@admin.register(Tag)
class TagAdmin(SoftDeleteMixin, admin.ModelAdmin):
    inlines = [ProductInline]
