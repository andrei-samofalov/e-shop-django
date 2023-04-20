from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatalogPaginator(PageNumberPagination):
    """Custom paginator for catalog representation"""
    page_size = 8

    def get_paginated_response(self, data):
        """
        Return response with ordered dict containing custom pagination info:
        `currentPage` and `lastPage`
        """
        page_amount = -(-self.page.paginator.count // self.page_size)

        return Response(
            OrderedDict(
                [
                    ('items', data),
                    ('currentPage', self.page.number),
                    ('lastPage', page_amount),
                ]
            )
        )
