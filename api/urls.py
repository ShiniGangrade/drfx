from django.urls import include, path

from .views import GoogleLogin, MicrosoftLogin, callback
from rest_auth.registration.views import SocialAccountListView

urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('rest-auth/google/connect/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/microsoft/connect/', MicrosoftLogin. as_view(), name='microsoft_callback'),

    path('rest-auth/callback/', callback, name='callback'),

    path('socialaccounts', SocialAccountListView.as_view(), name='social_account_list'),
]