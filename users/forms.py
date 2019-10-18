from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser  # , Role, Permissions

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        exclude = ('dashboards', 'grants')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        exclude = ('dashboards', 'grants')
