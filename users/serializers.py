from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'default_dashboard'
                  # , 'dashboards'
                  )

