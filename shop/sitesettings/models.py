"""
This module contains experimental site settings
that could be changed in admin panel
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Site settings that could be changed in admin section"""
    datetime_format = models.CharField(
        choices=settings.DATETIME_FORMATS,
        verbose_name=_('datetime formats'),
        help_text=_('choose datetime format that will be '
                    'represented through entire project'),
    )
    regular_delivery_cost = models.DecimalField(
        default=200,
        decimal_places=2,
        max_digits=10,
        verbose_name=_('cost of regular delivery'),
        help_text=_('choose regular delivery cost that will be '
                    'represented through entire project'),
    )
    express_delivery_cost = models.DecimalField(
        default=700,
        decimal_places=2,
        max_digits=10,
        verbose_name=_('cost of express delivery'),
        help_text=_('choose express delivery cost that will be '
                    'represented through entire project'),
    )
    popular_products_amt = models.PositiveSmallIntegerField(
        default=8,
        verbose_name=_('amount of popular products at main page'),
        help_text=_('choose amount of popular products that will be '
                    'represented at main page'),
    )
    limited_products_amt = models.PositiveSmallIntegerField(
        default=16,
        verbose_name=_('amount of limited products at main page'),
        help_text=_('choose amount of limited products that will be '
                    'represented at main page'),
    )
    banners_amt = models.PositiveSmallIntegerField(
        default=4,
        verbose_name=_('amount of banners at main page'),
        help_text=_('choose amount of banners that will be '
                    'represented at main page'),
    )
    cache_time = models.PositiveIntegerField(
        default=60 * 60 * 2,
        verbose_name=_('cache time'),
        help_text=_('choose time in seconds during which data will be cached')
    )

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')

    def save(self, *args, **kwargs):
        """Remove another instances of the class and save this"""
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return object of current settings from database"""
        return cls.objects.get()

    def __str__(self):
        return '{conf} №{id}'.format(
            conf=_("Configuration"), id=self.id
        )
