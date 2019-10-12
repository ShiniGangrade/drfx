from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm1(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        # fields = ('email', 'password1', 'password2', 'role')
        fields = ('email', 'role')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm1(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'role', 'default_dashboard')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    add_form = UserCreationForm1
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal info', {'fields': ('role',)}),
    #     # ('Permissions', {'fields': ('is_admin',)}),
    # )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'default_dashboard')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'default_dashboard')}
         ),
        # ('Personal info', {'fields': ('role',)}),
    )
    exclude = ('dashboards',)
    # form = CustomUserChangeForm
    form = UserChangeForm1
    model = CustomUser
    list_display = ['email', 'username', 'role', 'default_dashboard']

admin.site.register(CustomUser, CustomUserAdmin)