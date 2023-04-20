from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from sitesettings.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'datetime_format',
        'regular_delivery_cost',
        'express_delivery_cost',
        'popular_products_amt',
        'limited_products_amt',
        'banners_amt',
        'cache_time',
    ]
    list_display_links = 'datetime_format',
    list_editable = [
        'regular_delivery_cost',
        'express_delivery_cost',
        'popular_products_amt',
        'limited_products_amt',
        'banners_amt',
        'cache_time',
    ]
    actions = ['edit_configuration']

    @admin.action(description=_('Configure settings'))
    def edit_configuration(self, request, queryset):
        return redirect(f'{queryset[0].id}/change/')
