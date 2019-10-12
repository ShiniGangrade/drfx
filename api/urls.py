from django.urls import include, path
# from rest_framework_jwt.views import ObtainJSONWebToken

from .views import GoogleLogin, MicrosoftLogin, callback
from users.views import LoginView, LoginView1, LoginView2
# from users.views import LoginView2
from rest_auth.registration.views import SocialAccountListView
# from users.serializers import CustomJWTSerializer

urlpatterns = [
    path('users/', include('users.urls')),
    path('login/', LoginView2.as_view(), name='my_login'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('rest-auth/google/connect/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/microsoft/connect/', MicrosoftLogin. as_view(), name='microsoft_callback'),

    path('rest-auth/callback/', callback, name='callback'),

    path('socialaccounts', SocialAccountListView.as_view(), name='social_account_list'),
    # path('login1/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer), name='account_login'),
]