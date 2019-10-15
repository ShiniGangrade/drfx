from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        # fields = ('username', 'email', 'role', 'default_dashboard')
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['dashboards'].required = False

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # fields = ('username', 'email', 'role', 'default_dashboard')
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['dashboards'].required = False
