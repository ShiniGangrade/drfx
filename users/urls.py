from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, RoleViewSet, GrantViewSet, LoginView, demo, MicrosoftLogin  #,PasswordChangeView
from rest_auth.views import LogoutView

router = routers.DefaultRouter()
router.register(r'accounts', CustomUserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'grants', GrantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ad-login/', MicrosoftLogin. as_view(), name='microsoft_callback'),

    # path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('demo', demo, name='demo')
]
