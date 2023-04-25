from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from accounts.views import LogOutView, RegisterView

app_name = 'frontend'

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html"), name='index'),
    path('about/', TemplateView.as_view(template_name="frontend/about.html"), name='about'),
    path('account/', TemplateView.as_view(template_name="frontend/account.html"), name='account'),
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html"), name='cart'),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html"), name='catalog'),
    path('catalog/<int:pk>', TemplateView.as_view(template_name="frontend/catalog.html"), name='catalog-item'),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html"), name='history-order'),
    path('order-detail/<int:pk>/', TemplateView.as_view(template_name="frontend/oneorder.html"), name='order-detail'),
    path('order/', TemplateView.as_view(template_name="frontend/order.html"), name='order'),
    path('payment/', TemplateView.as_view(template_name="frontend/payment.html"), name='payment'),
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html"), name='payment-someone'),
    path('product/<int:pk>/', TemplateView.as_view(template_name="frontend/product.html"), name='product'),
    path('product/<slug:slug>/', TemplateView.as_view(template_name="frontend/product.html"), name='product-slug'),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html"), name='profile'),
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html"), name='progress-payment'),
    path('sale/', TemplateView.as_view(template_name="frontend/sale.html"), name='sale'),
    path('signin/', auth_views.LoginView.as_view(template_name="frontend/login.html"), name='signin'),
    path('logout/', LogOutView.as_view(template_name='frontend/logged_out.html'), name='logout'),
    path('signup/', RegisterView.as_view(), name='register'),
]
