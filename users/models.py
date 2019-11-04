from django.contrib.auth.models import AbstractUser

from djongo import models


class CustomUser(AbstractUser):

    role = models.CharField(blank=True, max_length=50, default='user')
    dashboards = models.ListField(default=[])
    # default_dashboard = models.CharField(blank=True, null=True, max_length=200)
    default_dashboard = models.DictField(default={})
    grants = models.ListField(default=[])

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Grant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
