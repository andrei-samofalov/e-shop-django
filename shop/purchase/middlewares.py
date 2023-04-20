from django.http import HttpRequest, HttpResponse

from purchase.cart import Cart


class SetCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.cart = Cart(request)
        response = self.get_response(request)
        return response
