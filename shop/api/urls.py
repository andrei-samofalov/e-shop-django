from django.urls import path

from api.catalog_api.views import (
    CatalogList,
    CategoryList,
    OfferList,
    ProductDetail,
    ProductListBanners,
    ProductListLimited,
    ProductListPopular,
    ReviewCreate,
    TagList,
)
from api.profile_api.views import AvatarSetView, PasswordChangeView, ProfileDetailView
from api.purchase_api.views import (
    BasketView,
    OrderActiveView,
    OrderListCreateView,
    OrderRetrieveConfirmView,
    PaymentView,
)

app_name = 'api'

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/avatar/', AvatarSetView.as_view(), name='avatar-change'),
    path('profile/password/', PasswordChangeView.as_view(), name='password-change'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/limited/', ProductListLimited.as_view(), name='product-limited'),
    path('banners/', ProductListBanners.as_view(), name='product-banners'),
    path('products/popular/', ProductListPopular.as_view(), name='product-popular'),
    path('products/<int:pk>/review/', ReviewCreate.as_view(), name='product-review'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('catalog/', CatalogList.as_view(), name='catalog-list'),
    path('sales/', OfferList.as_view(), name='offer-list'),
    path('orders/', OrderListCreateView.as_view(), name='order-detail'),
    path('orders/<int:pk>/', OrderRetrieveConfirmView.as_view(), name='order-create-retrieve'),
    path('orders/active/', OrderActiveView.as_view(), name='order-active'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('payment/', PaymentView.as_view(), name='payment'),

]
