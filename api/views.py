from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponse
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = '127.0.0.1:8000'



class MicrosoftLogin(SocialLoginView):
    adapter_class = MicrosoftGraphOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8000/accounts/google/microsoft/callback/'
    # callback_url = '127.0.0.1:8000'

    # @property
    # def callback_url(self):
    #     url = self.adapter_class(self.request).get_callback_url(
    #         self.request,
    #         None,
    #     )
    #     return url


def callback(request):
    print("callback function called")
    return HttpResponse("callback called")

# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
