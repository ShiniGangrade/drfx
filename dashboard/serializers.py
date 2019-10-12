from rest_framework import serializers
from . import models


class DashBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DashBoard
        fields = ('name',)
