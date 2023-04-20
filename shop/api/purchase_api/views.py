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
from api.purchase_api.service import is_payment_valid
from catalog.models import Product
from purchase.cart import Cart
from purchase.models import DeliveryType, Order, OrderItem


class PaymentView(APIView):
    @atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = self.request.data

        # getting orders which status is `awaiting payment`
        orders_for_pay = (
            Order.objects
            .prefetch_related('purchases')
            .filter(buyer=self.request.user.profile, status='awaiting payment')
        )
        card_number = data.get('number')

        # check if card number is valid, return bad request if not
        if not is_payment_valid(card_number):
            return Response(
                {'detail': 'card number is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # for each product in purchase decreasing stock if it enough,
        # otherwise - returning error
        purchases = OrderItem.objects.filter(order__in=orders_for_pay)
        errors = []
        for purchase in purchases.all():
            if purchase.product.stock < purchase.quantity:
                errors.append(f'not enough {purchase.product.title}')
            else:
                purchase.product.stock -= purchase.quantity
                purchase.product.save()

        if not errors:
            orders_for_pay.update(status='paid')
            self.request.cart.clear()
            return Response(status=status.HTTP_200_OK)

        return Response({'detail': errors}, status.HTTP_400_BAD_REQUEST)


class OrderActiveView(APIView):
    serializer_class = OrderSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request: Request, *args, **kwargs) -> Response:
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)

        user = self.request.user.profile
        active_order = get_object_or_404(Order, buyer=user, status='accepted')
        serializer = self.serializer_class(active_order)
        return Response(serializer.data)


class OrderRetrieveConfirmView(RetrieveModelMixin, GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_active=True)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = self.request.data
        user = self.request.user.profile

        order = Order.objects.select_related('buyer__user__profile').get(
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
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet[Order]:
        return (
            Order.objects
            .filter(buyer=self.request.user.profile)
            .order_by('-createdAt')
        )

    def post(self, request: Request, *args, **kwargs) -> Response:

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
    serializer_class = ProductShortSerializer

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
