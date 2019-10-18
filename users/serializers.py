""" todo - change fieldname case if needed"""

from rest_framework import serializers
from .models import CustomUser, Role, Grant


class CustomUserSerializer(serializers.ModelSerializer):
    dashboards = serializers.ListField(child=serializers.CharField(), required=False)
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

        instance.email = validated_data.get('email', instance.email)

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        instance.role = validated_data.get('role', instance.role)

        if 'grants' in validated_data:
            grants_string = validated_data['grants'][0][1:-1]
            grants_list = [i[1:-1] for i in grants_string.split(", ")] if grants_string else []
            instance.grants = grants_list

        instance.default_dashboard = validated_data.get('default_dashboard', instance.default_dashboard)

        if 'dashboards' in validated_data:
            dashboards_string = validated_data['dashboards'][0][1:-1]
            dashboards_list = [i[1:-1] for i in dashboards_string.split(", ")] if dashboards_string else []
            instance.dashboards = dashboards_list

        instance.save()
        return instance


class CustomRegisterUserSerializer(serializers.ModelSerializer):

    dashboards = serializers.ListField(child=serializers.CharField(), required=False)
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

        grants_string = validated_data.get('grants', '[]')[0][1:-1]
        grants_list = [i[1:-1] for i in grants_string.split(", ")] if grants_string else []
        validated_data["grants"] = grants_list

        role = validated_data.get('role', '')
        validated_data['role'] = role if role else 'user'

        dashboards_string = validated_data.get('dashboards', '[]')[0][1:-1]
        dashboards_list = [i[1:-1] for i in dashboards_string.split(", ")] if dashboards_string else []
        validated_data["dashboards"] = dashboards_list

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1024)
    token_type = serializers.CharField(max_length=100, default='Bearer')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = '__all__'
