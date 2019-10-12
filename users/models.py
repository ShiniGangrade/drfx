# from django.db import models
from django.contrib.auth.models import AbstractUser

from djongo import models
import djongo
from dashboard.models import DashBoard

class CustomUser(AbstractUser):

    role = models.CharField(blank=True, max_length=50, default='user')
    dashboards = models.ArrayReferenceField(to=DashBoard, on_delete=models.CASCADE, default=[])
    default_dashboard = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.email

