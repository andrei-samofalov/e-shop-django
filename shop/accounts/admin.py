from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from common_mixins.admin_mixins import SoftDeleteMixin


class ProfileInline(admin.StackedInline):
    """Profile inclusion for User model"""
    model = Profile
    can_delete = False


class UserAdmin(SoftDeleteMixin, BaseUserAdmin):
    """Base User admin representation"""
    ordering = ('date_joined',)
    list_display = (
        "pk",
        'username',
        'full_name',
        'email',
        'phone',
        'is_staff',
    )
    list_display_links = list_display
    inlines = [ProfileInline]

    @classmethod
    @admin.display(description=_('phone'))
    def phone(cls, obj: User):
        return obj.profile.phone

    @classmethod
    @admin.display(description=_('full name'))
    def full_name(cls, obj: User):
        return obj.profile.fullName


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#extending-the-existing-user-model
