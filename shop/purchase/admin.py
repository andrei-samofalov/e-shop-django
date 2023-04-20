from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common_mixins.admin_mixins import SoftDeleteMixin
from purchase.models import DeliveryType, Order, OrderItem  # OrderStatus, PaymentType


class OrderItemInline(admin.StackedInline):
    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'buyer',
        'deliveryType',
        'paymentType',
        'status',
        'city',
        'totalCost',
    )
    list_display_links = list_display
    inlines = [OrderItemInline]


@admin.register(DeliveryType)
class DeliveryTypeAdmin(SoftDeleteMixin, admin.ModelAdmin):
    pass
