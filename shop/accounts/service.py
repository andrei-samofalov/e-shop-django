from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest

from accounts.models import Profile


def authenticate_user(request: HttpRequest, cleaned_data: dict) -> User:
    """Get credentials from cleaned data and return authenticated user"""
    username = cleaned_data.get('username')
    password = cleaned_data.get('password1')
    return authenticate(
        request,
        username=username,
        password=password,
    )


def create_profile(user: User, cleaned_data: dict) -> None:
    """Get phone from cleaned data and create user's profile"""
    phone = cleaned_data.get('phone')
    Profile.objects.create(user=user, phone=phone)
