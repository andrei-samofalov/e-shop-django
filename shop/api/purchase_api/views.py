from django.contrib import messages
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.catalog_api.serializers import ProductShortSerializer
from api.purchase_api.serializers import OrderSerializer
from api.purchase_api.service import (
    is_payment_valid,
    check_stock_availability,
    reduce_product_stock_with_purchase_quantity
)
from catalog.models import Product
from purchase.cart import Cart
from purchase.models import DeliveryType, Order, OrderItem


class PaymentView(APIView):
    """POST for api/payment/"""
    @atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Check product stock for all orders,
        check user's card and finish payment
        """
        data = self.request.data

        # getting orders of request user which status is `awaiting payment`
        orders_for_pay = (
            Order.objects
            .prefetch_related('purchases')
            .filter(buyer=self.request.user.profile, status='awaiting payment')
        )
        card_number = data.get('number')

        # check if card number is valid, return bad request if not
        if not is_payment_valid(card_number):
            return Response(
                {'detail': 'card number %s is not valid' % card_number},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get all purchases in orders for pay
        # (it could be better to split purchases for each order)
        purchases = (
            OrderItem.objects
            .prefetch_related('product')
            .filter(order__in=orders_for_pay).all()
        )
        # check for stock availability of all products in purchases
        if errors := check_stock_availability(purchases) is False:
            # if ALL products have enough stock reduce it
            # with quantity in purchase
            reduce_product_stock_with_purchase_quantity(purchases)

            # change order statuses to `paid`
            orders_for_pay.update(status='paid')

            # delete all records from cart
            self.request.cart.clear()

            return Response(status=status.HTTP_200_OK)

        # if any of products doesn't have enough stock return bad request
        # with details
        return Response({'detail': errors}, status.HTTP_400_BAD_REQUEST)


class OrderActiveView(APIView):
    """GET for api/orders/active/"""
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)

        user = self.request.user.profile
        active_order = get_object_or_404(Order, buyer=user, status='accepted')
        serializer = self.serializer_class(active_order)
        return Response(serializer.data)


class OrderRetrieveConfirmView(RetrieveModelMixin, GenericAPIView):
    """GET and POST for api/orders/{id}/"""
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_active=True)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """"""
        data = self.request.data
        user = self.request.user.profile

        order = Order.objects.get(
            buyer=user, status='accepted'
        )

        order.status = 'awaiting payment'
        order.address = data.get('address', '')
        order.city = data.get('city', '')
        delivery_type = data.get('deliveryType', 'regular')
        dt = DeliveryType.objects.get(type=delivery_type)
        order.deliveryType = dt
        order.paymentType = data.get('paymentType', 'own online')
        order.save()
        messages.success(request, 'Заказ успешно создан')
        return Response(status=status.HTTP_201_CREATED)


class OrderListCreateView(ListCreateAPIView):
    """GET and POST for api/orders/"""
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet[Order]:
        return (
            Order.objects
            .filter(buyer=self.request.user.profile)
            .order_by('-createdAt')
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Create temp Order which would be finished in future"""
        if not request.user.is_authenticated:
            messages.error(request, 'Вам необходимо войти в свой аккаунт')
            return redirect(reverse('frontend:signin'))

        data = self.request.data

        data_ids = [d['id'] for d in data.values()]
        products = Product.objects.filter(id__in=data_ids)

        order, created = Order.objects.get_or_create(
            buyer=self.request.user.profile, status='accepted'
        )
        if created:
            self.request.cart.clear()
            for pr in products:
                pr_id = str(pr.id)
                OrderItem.objects.create(
                    order=order,
                    product=pr,
                    quantity=data[pr_id]['count'],
                    price=data[pr_id]['price'],
                )
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class BasketView(GenericAPIView):
    """GET, POST and DELETE for api/basket/"""
    serializer_class = ProductShortSerializer

    def __init__(self):
        super().__init__()
        self.cart = self.request.cart

    def get_queryset(self) -> QuerySet[Product]:
        cart = self.get_cart()
        return Product.objects.filter(id__in=cart.products.keys())

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.get_response()

    def post(self, request: Request, *args, **kwargs) -> Response:
        cart = self.get_cart()
        cart.add(*self.get_product_data())

        return self.get_response()

    def delete(self, request: Request, *args, **kwargs) -> Response:
        cart = self.get_cart()
        cart.reduce(*self.get_product_data())
        return self.get_response()

    def get_cart(self) -> Cart:
        return self.request.cart

    def get_product_data(self) -> tuple[Product, str]:
        body = self.request.data
        query = self.request.query_params

        product_id: str = body.get('id') or query.get('id')
        amount: str = body.get('count') or query.get('count')

        product = Product.objects.get(pk=product_id)

        return product, amount

    def get_response(self) -> Response:
        cart = self.get_cart()
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)
