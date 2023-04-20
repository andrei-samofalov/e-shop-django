from decimal import Decimal

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from catalog.models import Product
from purchase.choices import PaymentTypeChoices, StatusChoices, DeliveryChoices


class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        verbose_name=_('order'),
        related_name='purchases',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='purchases',
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_('quantity')
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name=_('price')
    )

    class Meta:
        verbose_name = _('product in order')
        verbose_name_plural = _('products in order')

    @property
    def total_cost(self):
        return Decimal(self.price * self.quantity)

    def __str__(self):
        return '{Order} id{o_id} - {Product} id{p_id} {association}'.format(
            Order=_('Order'),
            o_id=self.order_id,
            Product=_('Product'),
            p_id=self.product_id,
            association=_('association'),
        )


class DeliveryType(models.Model):
    """
    Delivery type and its cost.
    Note that there are only two types of delivery may be chosen.
    To add new type override `purchase.choices.DeliveryChoices` class.
    """
    type = models.CharField(
        choices=DeliveryChoices.choices,
        default=DeliveryChoices.regular,
        max_length=50,
        verbose_name=_('type')
    )
    cost = models.DecimalField(
        decimal_places=2, max_digits=5, verbose_name=_('cost of delivery')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('delivery type')
        verbose_name_plural = _('delivery types')

    def save(self, *args, **kwargs):
        """Save if the new type does not duplicate the existing ones"""
        if self.type not in [d.type for d in DeliveryType.objects.all()]:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.type


class Order(models.Model):
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('buyer'),
        null=True,
    )
    products = models.ManyToManyField(
        Product,
        through=OrderItem,
        through_fields=('order', 'product'),
        verbose_name=_('products'),
        blank=True,
    )
    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name=_('date of creation')
    )
    deliveryType = models.ForeignKey(
        DeliveryType,
        on_delete=models.PROTECT,
        verbose_name=_('delivery type'),
        related_name='orders',
        null=True,
    )
    paymentType = models.CharField(
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.own_online,
        verbose_name=_('type of payment'),
    )
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.accepted,
        verbose_name=_('status'),
    )
    city = models.CharField(max_length=100, default='', verbose_name=_('city'))
    address = models.TextField(default='', verbose_name=_('address'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def product_price(self, product: Product):
        oi = OrderItem.objects.get(product=product, order=self)
        return oi.price

    def product_count(self, product: Product):
        oi = OrderItem.objects.get(product=product, order=self)
        return oi.quantity

    @admin.display(description=_('total cost'))
    def totalCost(self):
        order_products = OrderItem.objects.filter(order=self)
        products_cost = sum([i.total_cost for i in order_products])
        if self.deliveryType.type == 'regular':
            delivery = self.deliveryType.cost if products_cost < 2000 else 0
        else:
            delivery = self.deliveryType.cost

        return delivery + products_cost

    def __str__(self):
        return '{buyer} {Order} id{o_id}'.format(
            buyer=self.buyer.fullName, Order=_('Order'), o_id=self.id
        )
