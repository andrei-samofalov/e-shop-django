from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

from accounts.path_resolvers import profile_avatar_path


class Profile(models.Model):
    """Profile for base User model"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user'),
        help_text=_('user that owns this profile')
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=profile_avatar_path,
        verbose_name=_("user's avatar"),
        help_text=_('avatar, file resolution must be *.jpeg, *.jpg or *.png')
    )
    phone = PhoneField(
        default='',
        blank=True,
        verbose_name=_('phone'),
        help_text=_('phone in international format')
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @property
    def fullName(self):
        """Return concatenated last name and first name of user"""
        return ' '.join([self.user.last_name, self.user.first_name])

    @fullName.setter
    def fullName(self, value):
        """Set last and first names of user passing rest of given string"""
        self.user.last_name, self.user.first_name, *_ = value.split()
        self.user.save()

    @property
    def email(self):
        """Return user's email"""
        return self.user.email

    @email.setter
    def email(self, value):
        """Set user's email"""
        self.user.email = value
        self.user.save()

    def set_avatar(self, avatar):
        """Set user's avatar"""
        self.avatar = avatar
        self.save()

    def __str__(self):
        return '{username}'.format(username=self.user.username.upper())
