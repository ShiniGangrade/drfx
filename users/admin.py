from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = get_user_model()

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'default_dashboard', 'dashboards')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'default_dashboard', 'dashboards')}
         ),
    )
    # list_display = ['email', 'username', 'role', 'default_dashboard']
    list_display = ['email', 'username', 'role']


admin.site.register(CustomUser, CustomUserAdmin)
