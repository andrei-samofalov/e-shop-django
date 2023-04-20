from django.http import HttpRequest, HttpResponse, HttpResponseNotFound


class APIHeadersMiddleware:
    """
    block all requests to api without header
    `X-HERE-I-AM` = `hello`
    this header MUST be included in all requests by frontend
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = self.get_response(request)

        if request.path.startswith('/api/'):
            if request.headers.get('X-HERE-I-AM') != 'hello':
                return HttpResponseNotFound()
            response.headers['X-HERE-I-AM'] = 'and hello to you'

        return response
