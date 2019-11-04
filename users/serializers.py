""" todo - change fieldname case if needed

for admin to change other users' passwords, use SetPasswordForm
for al users and admin to change their own passwords - use PasswordChangeForm

"""

from rest_framework import serializers
from .models import CustomUser, Role, Grant

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
import json


class DashboardSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    todo - check https://stackoverflow.com/questions/38388233/drf-allow-all-fields-in-get-request-but-restrict-post-to-just-one-field/38448743#38448743
    """
    default_dashboard = DashboardSerializer(required=False)
    # default_dashboard = serializers.DictField(child=DashboardSerializer(), required=False)

    dashboards = DashboardSerializer(many=True, required=False)
    grants = serializers.ListField(child=serializers.CharField(), required=False)

    # firstName = serializers.CharField(source='first_name')
    # lastName = serializers.CharField(source='last_name')
    # defaultDashboard = serializers.CharField(source='default_dashboard')

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'password',
            'first_name', 'last_name',
            'role', 'grants',
            'default_dashboard', 'dashboards'
        )
        extra_kwargs = {
            'password': {'write_only': True, "required": False},
            'username': {'read_only': True, "required": False},
        }

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CustomRegisterUserSerializer(serializers.ModelSerializer):

    default_dashboard = DashboardSerializer(required=False)
    dashboards = DashboardSerializer(many=True, required=False)
    # dashboards = serializers.ListField(child=serializers.CharField(), required=False)
    grants = serializers.ListField(child=serializers.CharField(), required=False)


    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'password',
            'first_name', 'last_name',
            'role', 'grants',
            'default_dashboard', 'dashboards'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        role = validated_data.get('role', '')
        validated_data['role'] = role if role else 'user'

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = '__all__'

# class PasswordChangeSerializer(serializers.Serializer):
#     old_password = serializers.CharField(max_length=128)
#     new_password1 = serializers.CharField(max_length=128)
#     new_password2 = serializers.CharField(max_length=128)
#
#     set_password_form_class = SetPasswordForm
#
#     def __init__(self, *args, **kwargs):
#         self.old_password_field_enabled = getattr(
#             settings, 'OLD_PASSWORD_FIELD_ENABLED', False
#         )
#         self.logout_on_password_change = getattr(
#             settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
#         )
#         super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
#
#         if not self.old_password_field_enabled:
#             self.fields.pop('old_password')
#
#         self.request = self.context.get('request')
#         self.user = getattr(self.request, 'user', None)
#
#     def validate_old_password(self, value):
#         invalid_password_conditions = (
#             self.old_password_field_enabled,
#             self.user,
#             not self.user.check_password(value)
#         )
#
#         if all(invalid_password_conditions):
#             raise serializers.ValidationError('Invalid password')
#         return value
#
#     def validate(self, attrs):
#         self.set_password_form = self.set_password_form_class(
#             user=self.user, data=attrs
#         )
#
#         if not self.set_password_form.is_valid():
#             raise serializers.ValidationError(self.set_password_form.errors)
#         return attrs
#
#     def save(self):
#         self.set_password_form.save()
#         if not self.logout_on_password_change:
#             from django.contrib.auth import update_session_auth_hash
#             update_session_auth_hash(self.request, self.user)
