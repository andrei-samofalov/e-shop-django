"""
This module contains serializers for order and purchase behavior
"""

from django.conf import settings
from rest_framework import serializers

from purchase.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'orderId',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
            'totalCost',
        )
        depth = 1

    orderId = serializers.SerializerMethodField('get_order_id')
    createdAt = serializers.SerializerMethodField('get_formatted_date')

    fullName = serializers.CharField(source='buyer.fullName')
    phone = serializers.CharField(source='buyer.phone')
    email = serializers.EmailField(source='buyer.email')

    products = serializers.SerializerMethodField('get_products')

    @classmethod
    def get_order_id(cls, obj: Order):
        return obj.pk

    @classmethod
    def get_formatted_date(cls, obj: Order):
        """
        Return formatted order creation date, format can be set in config--file
        """
        return obj.createdAt.strftime(settings.DATETIME_FORMAT)

    @classmethod
    def get_products(cls, obj: Order) -> list[dict]:
        """
        Return list of dicts containing product data for each product in order
        """
        return [
            {
                'href': pr.href,
                'images': [i.image.url for i in pr.images.all()],
                'title': pr.title,
                'description': pr.description,
                'price': obj.product_price(pr),
                'count': obj.product_count(pr),
            }
            for pr in obj.products.all()
        ]
