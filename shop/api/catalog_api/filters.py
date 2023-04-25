import django_filters as filters

from catalog.models import Product


class ProductFilter(filters.FilterSet):
    """
    Filterset for Product model
    Includes
        `freeDelivery`: filter by attribute freeDelivery
        `title`: filter title of product with case-insensitive containment test
        `minPrice`: filter product price with greater than or equal to value
        `maxPrice`: filter product price with less than or equal to value
        `available`: filter product stock with greater than zero
        `sort`: sorting queryset by product's
            price, creation date, amount of reviews, average rating
    """
    class Meta:
        model = Product
        fields = ['freeDelivery']

    sort = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('created_at', 'created'),
            ('_reviews', 'reviews'),
            ('_purchases', 'rating')
        )
    )
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    minPrice = filters.NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = filters.NumberFilter(field_name='price', lookup_expr='lte')
    available = filters.BooleanFilter(
        field_name='stock', method='check_availability'
    )
    freeDelivery = filters.BooleanFilter(
        field_name='freeDelivery', method='check_delivery'
    )

    @classmethod
    def check_availability(cls, queryset, name, value):
        """
        Check if product stock is greater than zero
        and return filtered queryset by this parameter
        """
        lookup = '__'.join([name, 'gt'])
        return queryset.filter(**{lookup: 0})

    @classmethod
    def check_delivery(cls, queryset, name, value):
        """
        Check if delivery is free
        and return filtered queryset by this parameter
        """
        if value is True:
            return queryset.filter(freeDelivery=True)
        return queryset
