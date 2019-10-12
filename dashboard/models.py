# from django.db import models
from django.contrib.auth.models import AbstractUser

from djongo import models
import djongo

class DashBoard(models.Model):

    name = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name

