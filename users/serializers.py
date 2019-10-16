""" todo - change fieldname case if needed"""

from rest_framework import serializers

from dashboard.serializers import DashBoardSerializer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    dashboards = DashBoardSerializer(many=True, required=False)
    # firstName = serializers.CharField(source='first_name')
    # lastName = serializers.CharField(source='last_name')
    # defaultDashboard = serializers.CharField(source='default_dashboard')

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'role', 'default_dashboard', 'dashboards')
        extra_kwargs = {
            'password': {'write_only': True, "required": False},
            'username': {'read_only': True, "required": False},
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.default_dashboard = validated_data.get('default_dashboard', instance.default_dashboard)
        instance.dashboards = validated_data.get('dashboards', instance.dashboards)

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class CustomRegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'role'
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

    # def update(self, instance, validated_data):
    #
    #     print("update 1")
    #
    #     instance.email = validated_data.get('email', instance.email)
    #     # instance.role = validated_data.get('role', instance.role)
    #     # instance.default_dashboard = validated_data.get('default_dashboard', instance.default_dashboard)
    #     # instance.dashboards = validated_data.get('dashboards', instance.dashboards)
    #     print("update 2")
    #     instance.save()
    #     print("update 3")
    #
    #     return instance


class CustomTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1024)
    token_type = serializers.CharField(max_length=100, default='Bearer')

