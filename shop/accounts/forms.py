from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phone_field import PhoneFormField, PhoneWidget


class UserProfileCreationForm(UserCreationForm):
    """Creation form for user registration with Profile fields included"""
    phone = PhoneFormField(widget=PhoneWidget(), required=False)

    class Meta(UserCreationForm):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
