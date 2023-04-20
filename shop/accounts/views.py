from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.views import RedirectURLMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.forms import UserProfileCreationForm
from accounts.service import authenticate_user, create_profile


class LogOutView(RedirectURLMixin, TemplateView):
    next_page = reverse_lazy('frontend:logged-out')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = UserProfileCreationForm
    template_name = 'frontend/register.html'
    success_url = reverse_lazy('frontend:profile')

    def form_valid(self, form: forms.Form):
        """
        Validate given form
        If validation passed, authenticate and login user,
        create user's Profile and return success response
        """
        # validate
        response = super().form_valid(form)
        # authenticate
        user = authenticate_user(self.request, form.cleaned_data)
        # login
        login(self.request, user)
        # create profile
        create_profile(user, form.cleaned_data)

        return response
