from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserViewSet
from .views import LoginView

router = routers.DefaultRouter()
router.register(r'', CustomUserViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
