from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PurchaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase'
    verbose_name = _('purchase')
