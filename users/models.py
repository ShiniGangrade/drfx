# from django.db import models
from django.contrib.auth.models import AbstractUser

from djongo import models
from dashboard.models import DashBoard

class CustomUser(AbstractUser):

    role = models.CharField(blank=True, max_length=50, default='user')
    dashboards = models.ArrayReferenceField(to=DashBoard, on_delete=models.CASCADE)
    default_dashboard = models.CharField(blank=True, null=True, max_length=50)
    # default_dashboard = models.ForeignKey(DashBoard, on_delete=models.CASCADE, related_name='default_dashboard')
    # default_dashboard = models.ArrayReferenceField(to=DashBoard, blank=True, null=True)

    def __str__(self):
        return self.username

