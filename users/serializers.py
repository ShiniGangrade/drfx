from rest_framework import serializers

from dashboard.serializers import DashBoardSerializer
from . import models


class UserSerializer(serializers.ModelSerializer):

    dashboards = DashBoardSerializer(many=True)

    class Meta:
        model = models.CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'default_dashboard'
                  , 'dashboards'
                  )


class CustomTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1024)
    token_type = serializers.CharField(max_length=100, default='Bearer')

