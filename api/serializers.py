from rest_framework import serializers


class UserJWTTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')
