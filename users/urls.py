from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    # path('api-token-auth/', views.ObtainAuthToken.as_view()),

]
