"""
This module contains session-based class Cart
Slightly modified Antonio Melé's cart
"""


import json
from decimal import Decimal

from django.conf import settings

from catalog.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        products = self.session.get(settings.CART_SESSION_ID)
        if not products:
            # save an empty cart in the session
            products = self.session[settings.CART_SESSION_ID] = {}
        self.products = products

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.products.keys()
        # get the product objects and add them to the cart
        qs_values = Product.objects.filter(id__in=product_ids).values()

        cart = self.products

        for product in qs_values:
            product_id = str(product['id'])
            product['count'] = cart.get(product_id)['count']
            product['price'] = cart.get(product_id)['price']
            yield Product(**product)

    def __repr__(self):
        return json.dumps(self.products)

    def add(self, product, quantity=1):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.products:
            self.products[product_id] = {
                'count': quantity,
                'price': str(product.price),
            }
        else:
            self.products[product_id]['count'] += int(quantity)

        self.save()

    def reduce(self, product, quantity):
        """Reduce product quantity up to removing from cart."""
        product_id = str(product.id)

        if product_id not in self.products:
            return

        if not quantity or self.products[product_id]['count'] <= 1:
            self.remove(product)
        else:
            self.products[product_id]['count'] -= int(quantity)

        self.save()

    def save(self):
        """Mark the session as "modified" to make sure it gets saved"""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.products:
            del self.products[product_id]
            self.save()

    def clear(self):
        """Remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_cost(self):
        """Return total cost of the cart"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.products.values()
        )

    def all(self):
        return [product for product in self.products.values()]
