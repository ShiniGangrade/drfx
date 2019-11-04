from django.urls import path

from . import views

urlpatterns = [
    path('sample-api/', views.sample_api, name='sample_api'),
]
