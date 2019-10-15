from django.urls import include, path

from . import views
from .views import LoginView


urlpatterns = [
    path('', views.UserListView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
]
