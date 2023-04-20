from typing import Literal

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


class SoftDeleteMixin:
    """Mixin for adding soft-delete actions to admin models"""
    actions = [
        'deactivate',
        'activate',
    ]

    @admin.display(description=_('Mark selected as active'))
    def activate(self, request: HttpRequest, queryset: QuerySet) -> None:
        """Activate selected items"""
        self.__handle(request, queryset, 'active')

    @admin.action(description=_('Mark selected as inactive'))
    def deactivate(self, request: HttpRequest, queryset: QuerySet) -> None:
        """Deactivate selected items"""
        self.__handle(request, queryset, 'inactive')

    def __handle(
            self,
            request: HttpRequest,
            queryset: QuerySet,
            action: Literal['active', 'inactive']
    ) -> None:
        """
        Handle action to set active-status for queryset,
        Send message to user with updated amount and action taken
        """
        updated = (
            queryset.update(is_active=False) if action == 'inactive'
            else queryset.update(is_active=True)
        )
        self.message_user(
            request,
            message=ngettext(
                singular=f"{updated} item was marked as {action}",
                plural=f"{updated} items were marked as {action}",
                number=updated,
            ),
            level=messages.SUCCESS,
        )
