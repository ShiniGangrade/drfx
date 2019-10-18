from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, RoleViewSet, GrantViewSet, LoginView

router = routers.DefaultRouter()
router.register(r'accounts', CustomUserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'grants', GrantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LoginView.as_view(), name='login'),
]
