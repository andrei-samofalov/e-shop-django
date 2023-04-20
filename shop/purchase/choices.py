from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentTypeChoices(models.TextChoices):
    own_online = _('own online')
    someone_online = _('someone online')


class StatusChoices(models.TextChoices):
    accepted = _('accepted')
    awaiting_payment = _('awaiting payment')
    paid = _('paid')
    delivered = _('delivered')


class DeliveryChoices(models.TextChoices):
    regular = _('regular')
    express = _('express')
